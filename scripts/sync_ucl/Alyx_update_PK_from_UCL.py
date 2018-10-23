from subjects.models import Sequence
from data.models import DataRepositoryType, DataRepository, DataFormat, DatasetType
import json


FILE_UCL_JSON_DUMP = '/var/www/alyx-dev/scripts/sync_ucl/cortexlab.json'
FILE_IBL_JSON_DUMP = '/var/www/alyx-dev/scripts/sync_ucl/ibl-alyx-dev.json'
FILE_IBL_JSON_DUMP_OUT = '/var/www/alyx-dev/scripts/sync_ucl/ibl-alyx-dev-pkucl.json'
CHECK_UCL_PK = True

pk_ibl2ucl_ = {
    '74d7a9d0-a031-4af0-93d1-61d98816c226':  '1fcc07ff-b17b-47bf-9eb6-e6d40ae3e1c9',  # Vglut1 WT subjects.sequence
    'e5d89025-c611-43d1-8a1b-04af9701483f':  '608d2996-737a-4e13-bd10-0bc28d653a36',  # Vglut1 MD subjects.sequence
    'f0d81608-ede8-47f9-afc5-e7bd1cf00e47':  'b91fa51a-4f23-4704-a03d-1737c742e164',  # Rasgrf Cre subjects.sequence
    '4d2cf793-6870-4a41-9fe2-963c461d3aeb':  'c4f3bbfb-5959-45a8-a52c-ba69d0a3c3ef',  # Rasgrf WT subjects.sequence
    'a4cbab57-4c50-44b6-ac7a-c646068b3b5b':  '8047d768-c04a-440e-91aa-f221719c4bc5',  # Fileserver data.datarepositorytype
    '5398fad6-18f9-4dfc-a3be-d1e9b3f31ada':  'bd237c2c-d114-49fa-adc8-cfaca4fc2f87',  # Cardboard box data.datarepositorytype
    '62ef5cca-f494-450b-9b4a-70203249fc1f':  '5a60da26-93ba-464a-8f4e-435220baaa6e',  # flatiron_cortexlab data.datarepository
    '5c0924d7-a4da-4e09-8de4-47d7bfad9bb0':  '1a3e32f5-fed8-458f-9440-198f368aaf7e',  # unknown data.dataformat
    '13df91c7-1277-4fb4-9341-24c36064682b':  '6fd398a0-8a3c-46c0-a9a2-e42f1c8f35d2',  # mj2 data.dataformat
    'f5c5bc03-2100-46d3-997e-a46457692c11':  '915c2d20-c77e-4c47-b4a5-d9eb6c782be1',  # m data.dataformat
    '8ea7e442-86b9-4db7-ba40-93c244ccd40a':  '9f923a3a-fe7f-4baa-bce1-6e0be4da78bb',  # json data.dataformat
    'b3674ad4-ed62-4dcf-bcd0-d46e03c27aa3':  'b0572461-af44-4979-b3c2-c9f12a8a0161',  # mat data.dataformat
    '63111539-1350-44f9-8c59-0619f5a8e787':  'c03e71e8-846a-42b2-9865-e9f950bb7806',  # bin data.dataformat
    '9a36f3ba-79f8-4e09-a4d9-ed9db0bbbf40':  'cdba2cad-6348-410f-bdd1-019a2b598d8c',  # csv data.dataformat
    'ac870204-c74c-4d65-a6a7-bb033212b334':  'e7b3d18f-5f58-4eea-994b-0e1f6ff87c2c',  # npy data.dataformat
    '1bb91b50-6216-4c7b-9230-ac2ecc041dbf':  '2a9092b0-c9fc-4740-bb43-28b254e3386e',  # _ibl_trials.feedbackType data.datasettype
    'f940a303-9b60-4d96-9499-bd747ba2635d':  '30717938-d036-40de-942f-b3dfe0c39c3b',  # _ibl_trials.rewardVolume data.datasettype
    'a529470c-a6dc-42ec-9075-5d8a1779492c':  '378aa050-4924-4a9b-9fe7-b7cf86dff93f',  # _ibl_trials.choice data.datasettype
    '9246461c-689c-463d-b5fe-363d33702c46':  '4cd7dcc9-62c1-4471-afa7-60544fc7e1ff',  # _ibl_trials.repNum data.datasettype
    'cecb3a60-ab2f-4bca-b90d-655f83f43cfc':  '54c9a39c-665c-4cf6-b06c-d7f18dae1e78',  # _ibl_wheel.position data.datasettype
    '2ea9f13d-5617-48e2-83c9-565cb8719ff9':  '5df90bef-df4f-4850-92b4-f0e43d619a0a',  # _ibl_trials.response_times data.datasettype
    'c36a150c-a8d6-420b-8e2e-4ca857d74fec':  '678a7e65-1dd1-4bff-b8c9-508e1f3a1cdc',  # _ibl_trials.intervals data.datasettype
    '9f38db94-825b-41a2-b08a-f4441648946b':  '72344745-c248-45e5-bf73-a9329c1720d2',  # _ibl_trials.stimOn_times data.datasettype
    '4f5ae5e6-0708-4b38-8756-7d1029c6c8c0':  '74c0120c-7515-478f-9725-53d587d86c49',  # _ibl_wheel.timestamps data.datasettype
    '5b2aa536-2675-4360-ad0a-a222e0103399':  '80e88e8b-7422-4970-af89-202c81b8f6c0',  # lfp.raw data.datasettype
    'bb9ec0e0-a16b-4358-8436-61b572560aac':  '81ea14a9-1512-4c1c-94e3-ccb7b42f6755',  # _ibl_wheelMoves.type data.datasettype
    '12a3a697-aaf3-44e5-8c08-27642b4f6305':  '9295f7a4-dd1b-440e-8ad0-53223aebab81',  # _ibl_trials.probabilityLeft data.datasettype
    'c097cf28-2312-46f9-b703-cdfd927b793c':  '979f9f7c-7d67-48d5-9042-a9000a8e66a2',  # _ibl_trials.contrastLeft data.datasettype
    '90b8a79d-4c51-4aa8-a999-14188c9410df':  '9d44dc73-67cd-4de7-b115-7d25723bc0da',  # _ibl_trials.contrastRight data.datasettype
    'c7448c4b-944d-48ad-993b-d8a1a2dd17ac':  'a60425e9-c5ab-4827-88a3-79b4eb68f989',  # _ibl_trials.feedback_times data.datasettype
    '0352c7f3-7412-4f3d-8f39-4ce4dfa3c333':  'd6584a34-f9dd-4870-ac02-0feb50fdf5f6',  # _ibl_trials.included data.datasettype
    '3d89bf13-f77a-476a-b31f-87cdde13c4c5':  'dce8e98a-ceb9-4f0b-955f-97e0b9bff497',  # unknown data.datasettype
    '359e3057-96b8-438f-b40a-26fdfa9de9bf':  'dea53510-d3e0-4b94-9739-2fe548a6f898',  # _ibl_wheelMoves.intervals data.datasettype
    'db5daf52-56c8-48c9-ac8c-d567f3f21d9f':  'e1542d34-9618-4369-aab7-0489484f6a12',  # _ibl_wheel.velocity data.datasettype
    '1010e897-e4fb-4732-8927-11bb8d2f9494':  'f7dbfad8-1cfc-459e-874f-4065cf9def86',  # _ibl_trials.goCue_times data.datasettype
}

# Load the database dump.
with open(FILE_UCL_JSON_DUMP, 'r') as f:
    DB_UCL = json.load(f)

if CHECK_UCL_PK:
    # modelClass = Sequence
    # fixture_name = modelClass._meta.label_lower
    # loop over all items and look at PK mismatches betweeen the two databases
    pk_ibl2ucl={}
    for item in DB_UCL:
        if item['model'] == 'subjects.sequence':
            print(item)
            dbitem = Sequence.objects.filter(name=item['fields']['name'])
            if dbitem.count() == 0: continue
            if item['pk'] != str(dbitem[0].pk):
                pk_ibl2ucl[str(dbitem[0].pk)] = item['pk']
                print('subjects.sequence: ' + str(item['pk']) + '  ' + str(dbitem[0].pk) + '  ' + item['fields']['name'])
        if item['model'] == 'data.datarepositorytype':
            dbitem = DataRepositoryType.objects.filter(name=item['fields']['name'])
            if dbitem.count() == 0: continue
            if item['pk'] != str(dbitem[0].pk):
                print('data.datarepositorytype: ' + str(item['pk']) + '  ' + str(dbitem[0].pk) + '  ' + item['fields']['name'])
                pk_ibl2ucl[str(dbitem[0].pk)] = item['pk']
        if item['model'] == 'data.datarepository':
            dbitem = DataRepository.objects.filter(name=item['fields']['name'])
            if dbitem.count() == 0: continue
            if item['pk'] != str(dbitem[0].pk):
                print('data.datarepository: ' + str(item['pk']) + '  ' + str(dbitem[0].pk) + '  ' + item['fields']['name'])
                pk_ibl2ucl[str(dbitem[0].pk)] = item['pk']
        if item['model'] == 'data.dataformat':
            dbitem = DataFormat.objects.filter(name=item['fields']['name'])
            if dbitem.count() == 0: continue
            if item['pk'] != str(dbitem[0].pk):
                print('data.dataformat: ' + str(item['pk']) + '  ' + str(dbitem[0].pk) + '  ' + item['fields']['name'])
                pk_ibl2ucl[str(dbitem[0].pk)] = item['pk']
        if item['model'] == 'data.datasettype':
            dbitem = DatasetType.objects.filter(name=item['fields']['name'])
            if dbitem.count() == 0: continue
            if item['pk'] != str(dbitem[0].pk):
                print('data.datasettype ' + str(item['pk']) + '  ' + str(dbitem[0].pk) + '  ' + item['fields']['name'])
                pk_ibl2ucl[str(dbitem[0].pk)] = item['pk']

    assert(sorted(pk_ibl2ucl) == sorted(pk_ibl2ucl_))  # strict comparison

# Regexp de sagouin this is not scalable 3 years down the road will have to split the file
# hopefully this PK conflict won't happen then
with open(FILE_IBL_JSON_DUMP) as f:
    text = f.read()

for k in (pk_ibl2ucl_):
    text = text.replace(k, pk_ibl2ucl_[k])

with open(FILE_IBL_JSON_DUMP_OUT, "w") as f:
    f.write(text)
