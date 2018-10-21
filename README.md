# ETL

We are going to store all the code for ETL here.

# Quickstart
Let's make sure every has the same setting to collaborate. After git clone, install flake8 hook. It automatically checks
[PEP8](http://pep8.org/) syntax for Python. Lastly, add DSN to your `~/.bashrc` and **NEVER** hardcode database
credentials in your code.



    git clone https://github.com/fccdsicapstone/etl.git
    cd etl

    flake8 --install-hook git
    git config --bool flake8.strict true

    # Make sure to replace USER, PASSWORD, and IP
    echo "export DSN='postgresql://USER:PASSWORD@IP:PORT/broadband'" >> ~/.bashrc
    source ~/.bashrc


# Postgresql setup
You can connect to Postgresql from [pgAdmin 4](https://www.pgadmin.org/). Let's insert all the data into `broadband`
database under `raw` schema. Once we cleanup each data set, we can move them to `public` schema.

As far as the SQL
naming convention, let's follow [this standard](https://stackoverflow.com/a/2878408/3128336). We write table name as
`lower_case_with_underscores` and SQL keywords `UPPER CASE`

For example,

    UPDATE my_table SET name = 5;

# How to read data from Postgresql with Python
## Method1 with sqlalchemy
    import os
    import pandas as pd
    from sqlalchemy import create_engine

    dsn = os.environ['DSN']
    engine = create_engine(dsn)

    query = """
    SELECT *
    FROM raw.fcc
    LIMIT 10
    """
    pd.read_sql(query, engine)

## Method2 with psycopg2
    import os
    import pandas as pd
    import psycopg2

    dsn = os.environ['DSN']
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()

    # specify your query
    sql = "SELECT * FROM raw.fcc LIMIT 10"  # example

    # execute your query
    cur.execute(sql)
    rows = cur.fetchall()
    print("The number of rows: ", cur.rowcount)

    # convert to dataframe
    df = pd.DataFrame(rows)

# How to insert a CSV file with Python

    import os
    import io
    import pandas as pd
    import psycopg2

    dsn = os.environ['DSN']
    conn = psycopg2.connect(dsn)
    curs = conn.cursor()

    df = pd.read_csv('some_file.csv')

    str_buf = io.StringIO()
    df.to_csv(str_buf, index=False, header=False, sep='\t')
    str_buf.seek(0)
    curs.copy_from(str_buf, 'raw.table_name', sep='\t')
    conn.commit()

# How to insert a CSV file with psql

    psql -h IP -p 5432 -U USERNAME -d broadband -c \copy raw.table_name from '~/Downloads/some_file.csv' with delimiter ',' csv header;

# BigQuery

FCC data is large (~400 million records) and PostgreSQL is slow for complex queries. So we also set up FCC data in [Google BigQuery](https://console.cloud.google.com/bigquery?project=fccdsicapstone-218522&authuser=1&organizationId=819335046878&p=fccdsicapstone-218522&page=project). All data can be queried from `broadband.fcc`.

`google-cloud-sdk` should be installed to use tools like `bq` and `gsutil`, and to resolve authorization problems. It comes pre-intalled on VM. On local machines, installation instruction can be found [here](https://cloud.google.com/sdk/docs/downloads-interactive).

Tranfer data example (via Google Cloud Engine Virtual Machine) to Google Cloud Storage
    
    ## In the VM (For internet speed. Avoid possible disconnection between local machine and storage caused by slow internet speed)
    curl -o http://transition.fcc.gov/form477/BroadbandData/Fixed/Jun17/Version%201/US-Fixed-with-Satellite-Jun2017.zip
    unzip US-Fixed-with-Satellite-Jun2017.zip
    gsutil -m cp fbd_us_with_satellite_jun2017_v1.csv gs://fcc-data-storage/fcc
    
Insert data from Google Cloud Storage to Google BigQuery Table (An empty table should be created beforehand either with console or [SQL query like this](https://github.com/fccdsicapstone/etl/blob/master/acs_ddl_googlebq.sql)

    ## In VM or Local Machine
    ## Skip the first line if there is header
    ## Set max_bad_records to a number (default 0)
    bq load -F , --source_format CSV --skip_leading_rows 1 --max_bad_records n -E UTF-8 broadband.fcc_201706 gs://fcc-data-storage/fcc/fbd_us_with_satellite_jun2017_v1.csv

In order to read data into pandas you must install `pandas-gbq`. 

    conda create --name capstone python=3.6
    source activate capstone
    conda install pandas
    conda install pandas-gbq --channel conda-forge
    conda install -c conda-forge google-cloud-sdk

Sign into the gcloud account - run `gcloud init` and follow the configuration & authentication instructions. Select your Columbia email as the account, and `fccdsicapstone-218522` as the project.

Now use the following structure to read data:

    import pandas as pd

    query = """
    SELECT
      file_date,
      state_county_code,
      AVG(max_ad_down) AS avg_max_ad_down
    FROM broadband.fcc
    GROUP BY file_date, state_county_code
    """

    pd.read_gbq(query, project_id='fccdsicapstone-218522', dialect='standard')
