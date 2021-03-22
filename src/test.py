import drive_utils.driveIO as driveIO

#print(driveIO.list_local_data_sources())
#print(driveIO.list_local_data())
#print(driveIO.list_local_data('atividade_parlamentar'))
#print(driveIO.list_remote_data_sources())
#print(driveIO.list_remote_data())
#sources = driveIO.list_data('atividade_parlamentar')
sources = driveIO.list_data()
for source in sources:
	print(sources[source])
driveIO.download_source('teste')