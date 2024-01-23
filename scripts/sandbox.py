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
r = requests.get("http://127.0.0.1:5001/atopile/us-central1/list_packages", json=data, timeout=5)
r.text

# %%
data = {
    "data": {
        "name": "stm32g4",
        "repo_url": "https://gitlab.atopile.io/packages/stm32g4"
    }
}
r = requests.post("http://127.0.0.1:5001/atopile/us-central1/add_package", json=data, timeout=5)
r.text

# %%
