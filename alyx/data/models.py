import structlog
from one.alf.spec import QC

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from alyx.settings import TIME_ZONE, AUTH_USER_MODEL
from actions.models import Session
from alyx.base import BaseModel, modify_fields, BaseManager, CharNullField, BaseQuerySet, ALF_SPEC

logger = structlog.get_logger(__name__)


def _related_string(field):
    return "%(app_label)s_%(class)s_" + field + "_related"


# Data repositories
# ------------------------------------------------------------------------------------------------

class NameManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class DataRepositoryType(BaseModel):
    """
    A type of data repository, e.g. local SAMBA file server; web archive; LTO tape
    """
    objects = NameManager()

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "<DataRepositoryType '%s'>" % self.name


class DataRepository(BaseModel):
    """
    A data repository e.g. a particular local drive, specific cloud storage
    location, or a specific tape.

    Stores an absolute path to the repository root as a URI (e.g. for SMB
    file://myserver.mylab.net/Data/ALF/; for web
    https://www.neurocloud.edu/Data/). Additional information about the
    repository can stored in JSON  in a type-specific manner (e.g. which
    cardboard box to find a tape in)
    """
    objects = NameManager()

    name = models.CharField(max_length=255, unique=True)
    repository_type = models.ForeignKey(
        DataRepositoryType, null=True, blank=True, on_delete=models.CASCADE)
    hostname = models.CharField(
        max_length=200, blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\.\-\_]+$',
                                   message='Invalid hostname',
                                   code='invalid_hostname')],
        help_text="Host name of the network drive")
    data_url = models.URLField(
        blank=True, null=True,
        help_text="URL of the data repository, if it is accessible via HTTP")
    timezone = models.CharField(
        max_length=64, blank=True, default=TIME_ZONE,
        help_text="Timezone of the server "
        "(see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)")
    globus_path = models.CharField(
        max_length=1000, blank=True,
        help_text="absolute path to the repository on the server e.g. /mnt/something/")
    globus_endpoint_id = models.UUIDField(
        blank=True, null=True, help_text="UUID of the globus endpoint")
    globus_is_personal = models.BooleanField(
        null=True, blank=True, help_text="whether the Globus endpoint is personal or not. "
        "By default, Globus cannot transfer a file between two personal endpoints.")

    def __str__(self):
        return "<DataRepository '%s'>" % self.name

    class Meta:
        verbose_name_plural = "data repositories"
        ordering = ('name',)


# Datasets
# ------------------------------------------------------------------------------------------------

class DataFormat(BaseModel):
    """
    A descriptor to accompany a Dataset or DataCollection, saying what sort of information is
    contained in it. E.g. "Neuropixels raw data, formatted as flat binary file" "eye camera
    movie as mj2", etc. Normally each DatasetType will correspond to a specific 3-part alf name
    (for individual files) or the first word of the alf names (for DataCollections)
    """

    objects = NameManager()

    name = models.CharField(
        max_length=255, unique=True,
        help_text="short identifying name, e.g. 'npy'")

    description = models.CharField(
        max_length=255, blank=True,
        help_text="Human-readable description of the file format e.g. 'npy-formatted square "
        "numerical array'.")

    file_extension = models.CharField(
        max_length=255,
        validators=[RegexValidator(r'^\.[^\.]+$',
                                   message='Invalid file extension, should start with a dot',
                                   code='invalid_file_extension')],
        help_text="file extension, starting with a dot.")

    matlab_loader_function = models.CharField(
        max_length=255, blank=True,
        help_text="Name of MATLAB loader function'.")

    python_loader_function = models.CharField(
        max_length=255, blank=True,
        help_text="Name of Python loader function'.")

    class Meta:
        verbose_name_plural = "data formats"
        ordering = ('name',)

    def __str__(self):
        return "<DataFormat '%s'>" % self.name


class DatasetType(BaseModel):
    """
    A descriptor to accompany a Dataset or DataCollection, saying what sort of information is
    contained in it. E.g. "Neuropixels raw data, formatted as flat binary file" "eye camera
    movie as mj2", etc. Normally each DatasetType will correspond to a specific 3-part alf name
    (for individual files) or the first word of the alf names (for DataCollections)
    """

    objects = NameManager()

    name = models.CharField(
        max_length=255, unique=True, blank=True, null=False,
        help_text="Short identifying nickname, e.g. 'spikes.times'")

    created_by = models.ForeignKey(
        AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.CASCADE,
        related_name=_related_string('created_by'),
        help_text="The creator of the data.")

    description = models.CharField(
        max_length=1023, blank=True,
        help_text="Human-readable description of data type. Should say what is in the file, and "
        "how to read it. For DataCollections, it should list what Datasets are expected in the "
        "the collection. E.g. 'Files related to spike events, including spikes.times.npy, "
        "spikes.clusters.npy, spikes.amps.npy, spikes.depths.npy")

    filename_pattern = CharNullField(
        max_length=255, unique=True, null=True, blank=True,
        help_text="File name pattern (with wildcards) for this file in ALF naming convention. "
        "E.g. 'spikes.times.*' or '*.timestamps.*', or 'spikes.*.*' for a DataCollection, which "
        "would include all files starting with the word 'spikes'. NB: Case-insensitive matching."
        "If null, the name field must match the object.attribute part of the filename."
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "<DatasetType %s>" % self.name

    def save(self, *args, **kwargs):
        """Ensure filename_pattern is lower case."""
        if self.filename_pattern:
            self.filename_pattern = self.filename_pattern.lower()
        return super().save(*args, **kwargs)


class BaseExperimentalData(BaseModel):
    """
    Abstract base class for all data acquisition models. Never used directly.

    Contains an Session link, to provide information about who did the experiment etc. Note that
    sessions can be organized hierarchically, and this can point to any level of the hierarchy
    """
    session = models.ForeignKey(
        Session, blank=True, null=True,
        on_delete=models.CASCADE,
        related_name=_related_string('session'),
        help_text="The Session to which this data belongs")

    created_by = models.ForeignKey(
        AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.CASCADE,
        related_name=_related_string('created_by'),
        help_text="The creator of the data.")

    created_datetime = models.DateTimeField(
        blank=True, null=True, default=timezone.now,
        help_text="The creation datetime.")

    generating_software = models.CharField(
        max_length=255, blank=True,
        help_text="e.g. 'ChoiceWorld 0.8.3'")

    provenance_directory = models.ForeignKey(
        'data.Dataset', blank=True, null=True,
        on_delete=models.CASCADE,
        related_name=_related_string('provenance'),
        help_text="link to directory containing intermediate results")

    class Meta:
        abstract = True


def default_dataset_type():
    return DatasetType.objects.get_or_create(name='unknown')[0].pk


def default_data_format():
    return DataFormat.objects.get_or_create(name='unknown')[0].pk


class Tag(BaseModel):
    objects = NameManager()
    name = models.CharField(max_length=255, blank=True, help_text="Long name", unique=True)
    description = models.CharField(max_length=1023, blank=True)
    protected = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    hash = models.CharField(blank=True, null=True, max_length=64,
                            help_text=("Hash of the data buffer, SHA-1 is 40 hex chars, while md5"
                                       "is 32 hex chars"))

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "<Tag %s>" % self.name


class Revision(BaseModel):
    """
    Dataset revision information
    """
    objects = NameManager()
    name_validator = RegexValidator(f"^{ALF_SPEC['revision']}$",
                                    "Revisions must only contain letters, "
                                    "numbers, hyphens, underscores and forward slashes.")
    name = models.CharField(max_length=255, blank=True, help_text="Long name",
                            unique=True, null=False, validators=[name_validator])
    description = models.CharField(max_length=1023, blank=True)
    created_datetime = models.DateTimeField(blank=True, null=True, default=timezone.now,
                                            help_text="created date")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "<Revision %s>" % self.name

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super(Revision, self).save(*args, **kwargs)


class DatasetQuerySet(BaseQuerySet):
    """A Queryset that checks for protected datasets before deletion"""

    def delete(self, force=False):
        if (protected := self.filter(tags__protected=True)).exists():
            if force:
                logger.warning('The following protected datasets will be deleted:\n%s',
                               '\n'.join(map(str, protected.values_list('name', 'session_id'))))
            else:
                logger.error(
                    'The following protected datasets cannot be deleted without force=True:\n%s',
                    '\n'.join(map(str, protected.values_list('name', 'session_id'))))
                raise models.ProtectedError(
                    f'Failed to delete {protected.count()} dataset(s) due to protected tags',
                    protected)
        super().delete()


class DatasetManager(BaseManager):
    def get_queryset(self):
        qs = DatasetQuerySet(self.model, using=self._db)
        qs = qs.select_related('dataset_type', 'data_format')
        return qs


@modify_fields(name={
    'blank': False,
})
class Dataset(BaseExperimentalData):
    """
    A chunk of data that is stored outside the database, most often a rectangular binary array.
    There can be multiple FileRecords for one Dataset, which will be different physical files,
    all containing identical data, with the same MD5.

    Note that by convention, binary arrays are stored as .npy and text arrays as .tsv
    """
    objects = DatasetManager()

    # Generic foreign key to arbitrary model instances allows polymorphic relationships
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField(help_text="UUID of an object whose type matches content_type.",
                                 null=True, blank=True)
    content_object = GenericForeignKey()

    file_size = models.BigIntegerField(blank=True, null=True, help_text="Size in bytes")

    md5 = models.UUIDField(blank=True, null=True,
                           help_text="MD5 hash of the data buffer")

    hash = models.CharField(blank=True, null=False, max_length=64,
                            help_text=("Hash of the data buffer, SHA-1 is 40 hex chars, while md5"
                                       "is 32 hex chars"))

    # here we usually refer to version as an algorithm version such as ibllib-1.4.2
    version = models.CharField(blank=True, null=False, max_length=64,
                               help_text="version of the algorithm generating the file")

    # the collection comprises session sub-folders
    collection_validator = RegexValidator(f"^{ALF_SPEC['collection']}$",
                                          "Collections must only contain letters, "
                                          "numbers, hyphens, underscores and forward slashes.")
    collection = models.CharField(blank=True, null=False, max_length=255,
                                  help_text='file subcollection or subfolder',
                                  validators=[collection_validator])

    dataset_type = models.ForeignKey(
        DatasetType, blank=False, null=False, on_delete=models.SET_DEFAULT,
        default=default_dataset_type)

    data_format = models.ForeignKey(
        DataFormat, blank=False, null=False, on_delete=models.SET_DEFAULT,
        default=default_data_format)

    revision = models.ForeignKey(
        Revision, blank=True, null=True, on_delete=models.SET_NULL)

    tags = models.ManyToManyField('data.Tag', blank=True, related_name='datasets')

    auto_datetime = models.DateTimeField(auto_now=True, blank=True, null=True,
                                         verbose_name='last updated')

    default_dataset = models.BooleanField(default=True,
                                          help_text="Whether this dataset is the default "
                                                    "latest revision")

    QC_CHOICES = [(e.value, e.name) for e in QC]
    qc = models.IntegerField(default=QC.NOT_SET, choices=QC_CHOICES,
                             help_text=' / '.join([str(q[0]) + ': ' + q[1] for q in QC_CHOICES]))

    @property
    def is_online(self):
        fr = self.file_records.filter(data_repository__globus_is_personal=False)
        return bool(fr.count() and any(fr.values_list('exists', flat=True)))

    @property
    def is_protected(self):
        return bool(self.tags.filter(protected=True).count())

    @property
    def is_public(self):
        return bool(self.tags.filter(public=True).count())

    @property
    def data_url(self):
        records = self.file_records.filter(data_repository__data_url__isnull=False, exists=True)
        # returns preferentially globus non-personal endpoint
        if records:
            order_keys = ('data_repository__globus_is_personal', '-data_repository__name')
            return records.order_by(*order_keys)[0].data_url

    def __str__(self):
        date = self.created_datetime.strftime('%d/%m/%Y at %H:%M')
        return "<Dataset %s %s '%s' by %s on %s>" % (
            str(self.pk)[:8], getattr(self.dataset_type, 'name', ''),
            self.name, self.created_by, date)

    def save(self, *args, **kwargs):
        # when a dataset is saved / created make sure the probe insertion is set in the reverse m2m
        super(Dataset, self).save(*args, **kwargs)
        if not self.collection:
            return
        self.clean_fields()  # Validate collection field
        from experiments.models import ProbeInsertion, FOV
        parts = self.collection.rsplit('/')
        if len(parts) > 1:
            name = parts[1]
            pis = ProbeInsertion.objects.filter(session=self.session, name=name)
            if len(pis):
                self.probe_insertion.set(pis.values_list('pk', flat=True))
            fovs = FOV.objects.filter(session=self.session, name=name)
            if len(fovs):
                self.field_of_view.set(fovs.values_list('pk', flat=True))

    def delete(self, *args, force=False, **kwargs):
        # If a dataset is protected and force=False, raise an exception
        # NB This is not called when bulk deleting or in cascading deletes
        if self.is_protected and not force:
            tags = self.tags.filter(protected=True).values_list('name', flat=True)
            tags_str = '"' + '", "'.join(tags) + '"'
            logger.error(f'Dataset {self.name} is protected by tag(s); use force=True.')
            raise models.ProtectedError(
                f'Failed to delete dataset {self.name} due to protected tag(s) {tags_str}', self)
        super().delete(*args, **kwargs)


# Files
# ------------------------------------------------------------------------------------------------
class FileRecordManager(models.Manager):
    def get_queryset(self):
        qs = super(FileRecordManager, self).get_queryset()
        qs = qs.select_related('data_repository')
        return qs


class FileRecord(BaseModel):
    """
    A single file on disk or tape. Normally specified by a path within an archive. If required,
    more details can be in the JSON
    """

    objects = FileRecordManager()

    dataset = models.ForeignKey(Dataset, related_name='file_records', on_delete=models.CASCADE)

    data_repository = models.ForeignKey(
        'DataRepository', on_delete=models.CASCADE)

    relative_path = models.CharField(
        max_length=1000,
        validators=[RegexValidator(r'^[a-zA-Z0-9\_][^\\\:]+$',
                                   message='Invalid path',
                                   code='invalid_path')],
        help_text="path name within repository")

    exists = models.BooleanField(
        default=False, help_text="Whether the file exists in the data repository", )

    class Meta:
        unique_together = (('data_repository', 'relative_path'),)

    @property
    def data_url(self):
        root = self.data_repository.data_url
        if not root:
            return None
        from one.alf.path import add_uuid_string
        return root + add_uuid_string(self.relative_path, self.dataset.pk).as_posix()

    def save(self, *args, **kwargs):
        """this is to trigger the update of the auto-date field"""
        super(FileRecord, self).save(*args, **kwargs)
        # Save the dataset as well to make sure the auto datetime in the dateset is updated when
        # associated file record is saved
        self.dataset.save()

    def __str__(self):
        return "<FileRecord '%s' by %s>" % (self.relative_path, self.dataset.created_by)


# Download table
# ------------------------------------------------------------------------------------------------

class Download(BaseModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    first_download = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    projects = models.ManyToManyField('subjects.Project', blank=True)

    class Meta:
        unique_together = (('user', 'dataset'),)

    def increment(self):
        self.count += 1
        self.save()

    def __str__(self):
        return '<Download of %s dataset by %s (%d)>' % (
            self.dataset.dataset_type.name, self.user.username, self.count)


def new_download(dataset, user, projects=()):
    d, _ = Download.objects.get_or_create(user=user, dataset=dataset)
    d.projects.add(*projects)
    d.increment()
    return d
