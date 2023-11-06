from sqlalchemy import create_engine , MetaData

#root = username mysql 
#12345678 = password mysql
#@localhost = localhost mysql si usas xammp o wamp es lo mismo
#3306 = puerto en uso de mysql 
engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/prueba')



meta_data = MetaData()

