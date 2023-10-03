# py-language

> A simple language written by Python.


### test.txt

```
let foo = 30 / 2;

const obj = {
    name: "Amy",
    y: 32,
    foo,
    complex: {
        is_human: true,
        is_girl: true,
    }
};

const names = ["Loya", "Amy", foo, foo = 5, ];

print(foo)

print(max(1, 0))
```

**Output**

```
$ python main.py test.txt

[{'type': 'number', 'value': 5.0}]
[{'type': 'number', 'value': 1.0}]
```

### func.txt

```
fn add(x, y) {
    fn subtract() {
        2
    }
    let result = x + y;
    print(result - 2)
    result + subtract()
}

const rst = add(10, 4);

print(rst)
```

**Output**

```
$ python main.py func.txt

[{'type': 'number', 'value': 12.0}]
[{'type': 'number', 'value': 16.0}]
```
