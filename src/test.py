import drive_utils.driveIO as driveIO

files = driveIO.list_remote_data()
for file in files:
	print('title: %s, kind: %s' % (file['title'], file['kind']))
	#for metadata in file:
	#	print(metadata, file[metadata])

local_files = driveIO.list_local_data_sources()
print(local_files)
print(driveIO.list_local_data())
print(driveIO.list_local_data('atividade_parlamentar'))
#print(driveIO.list_local_data('adsads'))
