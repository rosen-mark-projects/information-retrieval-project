import twitter

api = twitter.Api(consumer_key='0PR4TCmxevtwTmR7ELCatKZqR',
                  consumer_secret='Zb6hrXSaRRGhUksvv1UFyu6L2HwPsDHBvME0mYG3sex37BC6n0',
                  access_token_key='1225752542895857664-K56DSpMKDcMFhizcPYh42gLtZDMaUs',
                  access_token_secret='pb73NtkkRkkeUqfI48msKQZQLURZnOhTxAHh4CtIIaWRl')

print(api.VerifyCredentials())