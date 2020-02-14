# information-retrieval-project

## Development setup
    virtualenv -p python3 env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py develop

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

### To use Sentence encoder model from 
    wget https://tfhub.dev/google/universal-sentence-encoder/4
    tar -xvzf 4.tar.gz models/Sentence_encoder/embedded
    source env/bin/activate
	python models/Sentence_encoder train

