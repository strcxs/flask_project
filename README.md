# **Final Project - System23**

Backend repository for System23

>**IP: 34.87.73.138**

## **Notes**

- For testing project is work temporary: Run docker compose (use Makefile), then hit api with endpoint `/image` (in file `universal.py`). ex. `127.0.0.1:5000/image/image_name` or `34.142.211.35:5000/image/image_name`
- Models is created, feel free for add or delete it if you think that's right
- Documentation added in folder docs, feel free to add anything
- Folder `/admin`, `/utils`, `/docs`
- Allow CORS for all domains on all routes
- Column create_at > nullable=False
- Add class history as parent of class model
- Add ERD in `docs`
- Add JWT token, this functions add to `utils/auth_token.py`
  - encode function used when sign-in, this return a token, and it will be expired during 720 minutes or 12 hours
  - decode function used in every endpoint which contain `Authorization token` in request header, this return **User ID**, and it as `current_user` in parameter of endpoint
- Every endpoint within decorator `decode_auth_token` must fill `Authorization token` in header. Ex:
  - Authorization: Jwt xxxx.yyyy.zzzz

## **Link for tutorial**

- How to hash password? [How to store passwords securely using Werkzeug](https://techmonger.github.io/4/secure-passwords-werkzeug/ "techmonger.github.io")
- How to use errorhandler? [Python Flask: error and exception handling](https://instructobit.com/tutorial/112/Python-Flask:-error-and-exception-handling#:~:text=Error%20handling%20within%20a%20Flask%20mold%2C%20works%20much,as%20either%20global%20to%20your%20application%2C%20or%20mold-specific. "instructobit.com")
- How to use JWT?
  - [Introduction to JSON Web Tokens](https://jwt.io/introduction/ "jwt.io")
  - [Using JWT for user authentication in Flask](https://www.geeksforgeeks.org/using-jwt-for-user-authentication-in-flask/ "geeksforgeeks.org")
  - [Token-Based Authentication With Flask](https://realpython.com/token-based-authentication-with-flask/ "realpython.com")

## **How to run query use sql or orm**

If you forget how to run query use sql or orm, this could be test in file `routes/product`. Example:

```py
@products_bp.route("test", methods=["GET"])
def test_only():
    run_query(f"DELETE FROM products", True)

    run_query(f"INSERT INTO products VALUES ('{uuid.uuid4()}', 'cid1', 'tas', 20, 'lorem', 'S', 'used', 'image1', '[image1, image2]', '{datetime_format()}', 'admin')", True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="baju", price=100, detail="lorem ipsum", size="L", condition="used", image="image1", images_url=["image4", "image5"], create_at=datetime_format(), create_by="Ardi"), True)

    run_query(f"INSERT INTO products (id, category_id, name, price, size, condition, image, create_by) VALUES ('{uuid.uuid4()}', 'cid1', 'tas', 101, 'M',  'new', 'image2', 'Saya')", True)
    run_query(insert(Products).values(id=uuid.uuid4(), category_id="cid2", name="baju", price=100, detail="haloooooooo", condition="new", image="image2", create_by='Kamu'), True)

    query = run_query("SELECT * FROM products")
    orm = run_query(select(Products))

    return {
        "query": query,
        "orm": orm,
    },200
```

## **Connect to local with ssh (Windows/WSL)**

- cd .ssh
- ssh-keygen -t rsa -f [`FILENAME`] -C [`USERNAME`] -b 2048
- type [`FILENAME`].pub
- copy public key to GCP and add in security section
- finally you can connect via ssh using vs code

Test connect in cmd:

- ssh [`USERNAME`]@34.142.211.35 -i [`FILENAME`]

Test IP, run command:

- make build
- curl 34.142.211.35:5000/image

## **Endpoint section in requirements file**

>### Rully

- `home.py`: Home
- `auth.py`: Authentication
- `user.py`:
  - Profile page
  - Cart
  - Admin page

>### Faris

- `universal.py`: Universal
- `order.py`:
  - Profile page
  - Cart
  - Admin page
- `cart.py`:
  - Cart
  - Product detail page

>### Ardi

- `product.py`:
  - Product list
  - Product detail page
  - Admin page
- `category.py`:
  - Product list
  - Admin page
