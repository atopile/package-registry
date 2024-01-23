## Dev Guide

### Setup

`npm install -g firebase-tools` (or via yarn) for firebase CLI

### Common issues

#### `>  DEBUG:google.auth._default:Checking /Users/mattwildoer/.config/gcloud/application_default_credentials.json for explicit credentials as part of auth process...`

Do the `gcloud auth application-default login` as suggested in the error message.

If that fails, it may be because something has mucked up which default credentials it's trying to hit. Try `export GOOGLE_APPLICATION_CREDENTIALS="~/.config/gcloud/application_default_credentials.json"`

Otherwise it may also help to do a `firebase logout && firebase login` to reset the credentials.

#### `There was an error when calling the Cloud Function FirebaseError: Response is missing data field. FirebaseError: Response is missing data field.`

Your response dict needs a field named `data`... - I saw this written nowhere in the offical docs

https://csiandal.medium.com/firebase-function-error-response-is-missing-data-field-2c27768e0bd


#### CORS

This fixes it right up

```python
@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"],
        cors_methods=["get", "post"],
    )
)
```
