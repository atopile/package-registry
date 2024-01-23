# %%
"https://github.com/atopile/atopile/".split("/")
# %%
a,b,c = "ab"
# %%
import requests
import json

# %%
data = {
    # "name": "test2",
}
r = requests.get("https://atopile--pr2-mawildoer-package-re-k1a277l1.web.app/atopile/us-central1/list_packages", json=data, timeout=5)
r.text

# %%
data = {
    "name": "test-2",
    "repo_url": "https://github.com/atopile/module-template"
}
r = requests.post("http://127.0.0.1:5001/atopile/us-central1/add_package", json=data, timeout=5)
r.text

# %%
