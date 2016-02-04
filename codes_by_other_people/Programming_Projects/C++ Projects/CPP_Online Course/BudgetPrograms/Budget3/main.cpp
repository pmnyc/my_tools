// BUDGET3 - Budget program with inheritance and
//           late binding (aka, polymorphism). A
//           single function can handle both checking
//           and savings accounts (and any other
//           accounts that you might invent in the
//           future).
//
//           In addition, this version stored accounts
//           in a linked list rather than a fixed array
//           in order to avoid the limitation of a
//           fixed maximum number of objects.

#include <cstdio>
#include <cstdlib>
#include <iostream>

#include "AccountLinkedList.h"
using namespace std;
using namespace Lists;

// Account - this abstract class incorporates properties
//          common to both account types: Checking and
//          Savings. However, it's missing the concept
//          withdrawal(), which is different between the two
class Account
{
  public:
    Account(AccountLinkedList* pList, int accNo)
       : node(pList, this), accountNumber(accNo), balance(0)
    {
      count++;
    }

    // access functions
    int accountNo() { return accountNumber; }
    double acntBalance() { return balance; }
    static int noAccounts() { return count; }

    // transaction functions
    void deposit(double amount) { balance += amount; }
    virtual bool withdrawal(double amount)
    {
        if (balance < amount )
        {
             cout << "Insufficient funds: balance " << balance
                  << ", withdrawal "                << amount
                  << endl;
              return false;
        }
        balance -= amount;
        return true;
    }

    // display function for displaying self on 'cout'
    void display()
    {
        cout << type()
             << " account " << accountNumber
             << " = "   << balance
             << endl;
    }
    virtual const char* type() = 0;

  protected:
    // the node retains the linked list information
    Node node;

    static int count;             // number of accounts
    unsigned accountNumber;
    double   balance;
};

// allocate space for statics
int Account::count = 0;

// Checking - this class contains properties unique to
//            checking accounts. Not much left, is there?
class Checking : public Account
{
  public:
    Checking(AccountLinkedList* pLL, unsigned accNo)
      : Account(pLL, accNo) { }

    // overload pure virtual functions
    virtual bool withdrawal(double amount);
    virtual const char* type() { return "Checking"; }
};

// withdrawal - overload the Account::withdrawal() member
//              function to charge a 20 cents per check if
//              the balance is below $500
bool Checking::withdrawal(double amount)
{
    bool success = Account::withdrawal(amount);

    // if balance falls too low, charge service fee
    if (success && balance < 500.00)
    {
        balance -= 0.20;
    }
    return success;
}

// Savings - same story as Checking except that it also
// has a unique data member
class Savings : public Account
{
  public:

    Savings(AccountLinkedList* pLL, unsigned accNo)
      : Account(pLL, accNo), noWithdrawals(0) {}

    // transaction functions
    virtual bool withdrawal(double amount);
    virtual const char* type() { return "Savings"; }

  protected:
    int noWithdrawals;
};

// withdrawal - overload the Account::withdrawal() member
//              function to charge a $5.00 fee after the first
//              withdrawal of the month
bool Savings::withdrawal(double amount)
{
    if (++noWithdrawals > 1)
    {
        balance -= 5.00;
    }
    return Account::withdrawal(amount);
}

// prototype declarations
unsigned getAccntNo();
void     process(Account* pAccount);
void     getAccounts(AccountLinkedList* pLinkedList);
void     displayResults(AccountLinkedList* pLinkedList);


// main - accumulate the initial input and output totals
int main(int argcs, char* pArgs[])
{
    // create a link list to attach accounts to
    AccountLinkedList* pLinkedList = new AccountLinkedList();

    // read accounts from user
    getAccounts(pLinkedList);

    // display the linked list of accounts
    displayResults(pLinkedList);

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// getAccounts - load up the specified array of Accounts
void getAccounts(AccountLinkedList* pLinkedList)
{
    Account* pA;

    // loop until someone enters 'X' or 'x'
    char   accountType;     // S or C
    while (true)
    {
        cout << "Enter S for Savings, "
             << "C for Checking, X for exit:";
        cin >> accountType;
        switch (accountType)
        {
          case 'c':
          case 'C':
            pA = new Checking(pLinkedList, getAccntNo());
            break;

          case 's':
          case 'S':
            pA = new Savings(pLinkedList, getAccntNo());
            break;

          case 'x':
          case 'X':
            return;

          default:
            cout << "I didn't get that.\n";
        }

        // now process the object we just created
        process(pA);
    }
}

// displayResults - display the accounts found in the
//                  Account link list
void displayResults(AccountLinkedList* pLinkedList)
{
    // now present totals
    double total = 0.0;
    cout << "\nAccount totals:\n";
    for (Node* pN = Node::firstNode(pLinkedList);
               pN != 0;
               pN = pN->nextNode())
    {
        Account* pA = pN->currentAccount();
        pA->display();
        total += pA->acntBalance();
    }
    cout << "Total worth = " << total << "\n";
}

// getAccntNo - return the account number to create account
unsigned getAccntNo()
{
    unsigned accntNo;
    cout << "Enter account number:";
    cin  >> accntNo;
    return accntNo;
}

// process(Account) - input the data for an account
void process(Account* pAccount)
{
    cout << "Enter positive number for deposit,\n"
         << "negative for withdrawal, 0 to terminate\n";
    double transaction;
    while(true)
    {
        cout << ":";
        cin >> transaction;
        if (transaction == 0)
        {
            break;
        }

        // deposit
        if (transaction > 0)
        {
            pAccount->deposit(transaction);
        }
        // withdrawal
        if (transaction < 0)
        {
            pAccount->withdrawal(-transaction);
        }
    }
}

