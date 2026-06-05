import modal

app = modal.App("example-hello-world")


@app.function()
def f():
    print("Hello world!")


@app.function()
def g():
    print("Goodbye world!")


if __name__ == "__main__":
    with app.run():
        f.remote()
        g.remote()
