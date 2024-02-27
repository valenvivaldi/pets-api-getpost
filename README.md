# pets-api-getpost
A PetStore simple API to test. Only has GET &amp; POST methods.


## Generate docker image
```bash
docker build -t pets-api-getpost .
```

## Run docker container, with api in port 9999 for example. With a custom name.
```bash
docker run -d --name api-custom-name -p 8899:8899  pets-api-getpost
```