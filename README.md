s# information-retrieval-project

## Development setup
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt

Create `.env` file in root path replacing the bracketed values:

	POSTGRES_USER=<USERNAME>
	POSTGRES_PASS=<PASSWORD>
	POSTGRES_HOST=<HOST>
	POSTGRES_DB=<NAME>
    CONSUMER_KEY=<>
    CONSUMER_SECRET=<>
    ACCESS_TOKEN=<>
    ACCESS_TOKEN_SECRET=<>


### Create DB, search and fill tweets in DB
    source env/bin/activate
	python create_database
	python fill_database
