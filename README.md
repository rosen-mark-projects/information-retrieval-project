# information-retrieval-project

## Development setup
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt

Create `.prod.env` file in root path replacing the bracketed values:

	SECRET_KEY=<the output of `openssl rand -base64 42`>
	POSTGRES_USER=<USERNAME>
	POSTGRES_PASS=<PASSWORD>
	POSTGRES_HOST=<HOST>
	POSTGRES_DB=<NAME>
    CONSUMER_KEY=<>
    CONSUMER_SECRET=<>
    ACCESS_TOKEN=<>
    ACCESS_TOKEN_SECRET=<>


### Create DB
    source env/bin/activate
	python create_database
