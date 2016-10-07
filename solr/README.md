##########################
Constants to be considered
##########################

SOLR_HOME = '~/solr-5.5.0'



#################
How to start solr
#################
1. Change the directory
    cd SOLR_HOME

2. Start the solr instance
bin/solr start


###################
How to create cores
###################

1. Create a folder with the name of the required core in the folder SOLR_HOME/server/solr

2. Create a folder name 'conf' in the folder, you just created. You could copy one of the folders in configsets/<example>.

3. Go the GUI of solr and select 'core-admin' from the left menu.

4. Enter the name of the folder in the fields asking for 'name' and 'instanceDir'. You may wish to leave the defaults
   for the other fields.
   For example : datadir - data; config - solrconfig.xml; schema - schema.xml

5. Click 'Add Core' button to create the solr.

6. You may verify the core instantiation by looking into the folder you just created in Step 1. You would see the datadir in the folder. Further you can also see the 'core.properties' file with the value you just entered.

HAPPY INDEXING!!