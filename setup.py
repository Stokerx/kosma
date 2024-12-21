from rules import Validator

def main():
    print("Hello from kosma!")


if __name__ == "__main__":
    main()


rules =  {
    'email' : ['required', 'email'],
    'password' : ['required','string','min:8'],
    'age' : ['required','integer','min:18'],
}


validator = Validator(rules)