-- For mysql

--SOURCE <%os.sep.join((os.getcwd(), BUILD_DIR, TABLE_CREATE_FILE))%>;
<+ files = list(src_files) #
|= files.remove(TABLE_CREATE_FILE) #
->
<+ for name in files:
SOURCE <%os.sep.join((os.getcwd(), BUILD_DIR, name))%>;
->
