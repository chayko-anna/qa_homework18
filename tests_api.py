import allure
from selene import browser, have, be
from selene.core.query import value
import requests
from allure_commons.types import AttachmentType

login = "example1200@example.com"
pwd = "123456"
url = "https://demowebshop.tricentis.com/"

def test_auth_using_api():
    with allure.step("API authorisation"):
        res = requests.post(url=url + "login",
                            data={"Email": login,
                                  "Password": pwd,
                                  "Remember me": False},
                            allow_redirects=False)
        allure.attach(body=res.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=res.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(res.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step("Get cookie from API"):
        cookie = res.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Set cookie from API"):
        browser.open(url)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(url)


def test_adding_to_cart_using_api():
    with (allure.step("Add item to a cart")):
        payload = "addtocart_31.EnteredQuantity: 1"
        res = requests.post(
            url=url + "addproducttocart/details/31/1",
            data=payload,
            headers={'Accept': 'application/json'}
        )
        allure.attach(body=res.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=res.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(res.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step("Get cookie from API"):
        cookie = res.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(url + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(url + "cart")

    with allure.step("Check item visibility in cart"):
        browser.element("[class='page shopping-cart-page'").should(have.text("14.1-inch Laptop"))


def test_remove_item_from_cart():
    with (allure.step("Add item to a cart")):
        payload = "addtocart_31.EnteredQuantity: 1"
        res = requests.post(
            url=url + "addproducttocart/details/31/1",
            data=payload,
            headers={'Accept': 'application/json'}
        )
    with allure.step("Get cookie from API"):
        cookie = res.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(url + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(url + "cart")

    with allure.step("Delete item from cart"):
        item_value = browser.element("[name='removefromcart'").get(value)
        payload = {f"removefromcart": {item_value},
                   "updatecart": 'Update shopping cart',
                   "discountcouponcode": '',
                   "giftcardcouponcode": '',
                   }
        res = requests.post(url + "cart", data=payload)
        allure.attach(body=res.url, name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=res.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(res.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step("Get cookie from API"):
        cookie = res.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(url + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(url + "cart")

    with allure.step("Check item is not in cart"):
        browser.element("[class='page shopping-cart-page'").should(have.text("Your Shopping Cart is empty!"))
