import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

root = tk.Tk()
root.title("PoS by Justyn Shelby")
root.geometry("1280x720")

class Shopping_Cart():

    def __init__(self):
        self.cart = []
        self.total = 0
        self.size = 0
    
    def add(self, item):
        if item.sku not in (x.sku for x in self.cart):
            self.cart.append(Shopping_Cart_Item(item.sku, item.name, 1, item.price))
            self.total += item.price
            self.size += 1
        else:
            shopping_cart_item = self.cart[[x.sku for x in self.cart].index(item.sku)]
            shopping_cart_item.qty += 1
            self.total += shopping_cart_item.price
        self.cart.sort(key = lambda x: x.price * x.qty, reverse=True)

    def remove(self, item):
        if item in self.cart():
            self.cart.remove(item)
            self.total -= item.price
            self.size -= 1

    def update(self, difference):
        self.total += difference
        self.cart.sort(key = lambda x: x.price * x.qty, reverse=True)

shopping_cart = Shopping_Cart()
    
class Product():

    def __init__(self, name: str, sku: int, price: float, qty: int):
        self.name = name
        self.sku = sku
        self.price = price
        self.qty = qty

class Shopping_Cart_App():

    def __init__(self, master, shopping_cart):
        self.master = master
        self.shopping_cart = shopping_cart
        self.page = 0
        self._reload()

    def _reload(self):
        frame = tk.Frame(master=self.master, relief=tk.GROOVE, borderwidth=2)
        tk.Label(master=frame, text="Shopping Cart").pack()
        shopping_cart_item_frame(Shopping_Cart_Item(None, "Item", "Qty", "Price"), frame, borderwidth=1).pack()
        items_frame = tk.Frame(master=frame, background="pink", height=1)
        for i, item in enumerate([x for x in self.shopping_cart.cart if x.qty > 0][14 * self.page:14 * self.page + 14]):
            print(f"{item.name=} {item.qty=}")
            shopping_cart_item_frame(item, items_frame).grid(column=0, row=i)
        page_buttons = tk.Frame(master=frame)
        tk.Button(master=page_buttons, text="<", width="2", height="1", relief=tk.RAISED, borderwidth=1, command=self.dec_page).pack(side=tk.LEFT)
        tk.Label(master=page_buttons, text=f"Page {self.page + 1}/{self.shopping_cart.size // 14 + 1}", width=5).pack(side=tk.LEFT)
        tk.Button(master=page_buttons, text=">", width="2", height="1", relief=tk.RAISED, borderwidth=1, command=self.inc_page).pack(side=tk.LEFT)
        total_frame = tk.Frame(master=frame, relief=tk.GROOVE, borderwidth=1)
        tk.Label(master=total_frame, text="Total", width=30, height=2).grid(row=0, column=0)
        tk.Label(master=total_frame, text=f"${self.shopping_cart.total:.2f}", width=10, height=2).grid(row=0, column=1)
        items_frame.pack()
        total_frame.pack(side=tk.BOTTOM)
        page_buttons.pack(side=tk.BOTTOM)
        self.frame = frame
        self.frame.grid(row=1, column=0, sticky="nsw", padx="3", pady="3")

    def inc_page(self):
        if self.page < shopping_cart.size // 14:
            self.page += 1
            self.reload()

    def dec_page(self):
        if self.page - 1 >= 0:
            self.page -= 1
            self.reload()

    def reload(self):
        self.frame.destroy()
        self._reload()

def edit_quantity(item, event):
    new_qty = tk.StringVar()
    entry = tk.Entry(master=root, width=2, textvariable=new_qty)
    entry.bind("<Return>", lambda x:destroy(item))
    entry.place(x=root.winfo_pointerx()- 20, y=root.winfo_pointery() - 85)

    def destroy(item):
        new_qty_int = int(new_qty.get())
        if new_qty_int < 0:
            pass
        else:
            difference = new_qty_int - item.qty
            item.qty = new_qty_int
            shopping_cart.update(item.price * difference)
            shopping_cart_app.reload()
        entry.destroy()

def shopping_cart_item_frame(item, master, borderwidth=0):
    frame = tk.Frame(master=master, relief=tk.GROOVE, borderwidth=borderwidth)
    tk.Label(height="2", master=frame, text=item.name, width=25).grid(row=0, column=0)
    quantity = tk.Label(master=frame, text=item.qty, width=5)
    quantity.bind("<Button-1>", partial(edit_quantity, item)) # partial(edit_quantity), item
    quantity.grid(row=0, column=1)
    total_price = f"{item.price*item.qty:.2f}" if type(item.qty) == int else item.price
    tk.Label(master=frame, text=total_price, width=10).grid(row=0, column=2)
    return frame

class Shopping_Cart_Item():

    def __init__(self, sku, name, qty, price):
        self.sku = sku
        self.name = name
        self.qty = qty
        self.price = price

shopping_cart_app = Shopping_Cart_App(root, shopping_cart)

def main():
    information_frame = tk.Frame(relief=tk.GROOVE, borderwidth=2)
    title = tk.Label(master=information_frame, text="PoS Program", height="1", font=("Arial", 25))
    title.pack()

    product_select_frame = tk.Frame(relief=tk.GROOVE, borderwidth=2)
    page_select_frame = tk.Frame(master=product_select_frame, relief=tk.GROOVE, borderwidth=2)
    pagstitle = tk.Label(master=page_select_frame, text="Page Selection")
    pagstitle.pack(fill="x")
    page_select_frame.pack(fill="x")
    # Products Label
    prostitle = tk.Label(master=product_select_frame, text="Product Selection")
    prostitle.pack(fill="x")
    # Products
    product_grid_frame = tk.Frame(master=product_select_frame, width="107")
    product_grid_frame.pack()
    def add_to_cart(i):
        shopping_cart.add(i)
        shopping_cart_app.reload()
    for i, product in enumerate(inventory):
        product_button = tk.Button(
            text=product.name,
            width="15",
            height="5",
            master=product_grid_frame,
            relief=tk.RAISED,
            borderwidth=1,
            command=partial(add_to_cart, product)
        )
        product_button.grid(column=i % 5, row=i // 5, padx=3, pady=3)

    information_frame.grid(row=0, column=0, columnspan=2, sticky="new", padx="3", pady="3")
    shopping_cart_app.reload()
    product_select_frame.grid(row=1, column=1, sticky="nsew", padx="3", pady="3")

    root.columnconfigure(1, weight=3)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    inventory = [Product("Apple", 1, 0.99, 5),
                Product("Banana", 2, 0.25, 10),
                Product("Strawberry", 3, 1.10, 5),
                Product("Lettuce", 4, 0.35, 10),
                Product("Potato", 5, 1.50, 5),
                Product("Celery", 6, 2.80, 10),
                Product("Carrot", 7, 0.20, 5),
                Product("Orange", 8, 0.40, 8),
                Product("Avocado", 9, 1.25, 1),
                Product("Blueberry", 10, 0.10, 3)]
    
    """inventory += [Product("Apple", 11, 0.99, 5),
                Product("Banana", 12, 0.25, 10),
                Product("Strawberry", 13, 1.10, 5),
                Product("Lettuce", 14, 0.35, 10),
                Product("Potato", 15, 1.50, 5),
                Product("Celery", 16, 2.80, 10),
                Product("Carrot", 17, 0.20, 5),
                Product("Orange", 18, 0.40, 8),
                Product("Avocado", 19, 1.25, 1),
                Product("Blueberry", 110, 0.10, 3)]"""

    """for item in inventory:
        shopping_cart.add(item)"""
    
    main()