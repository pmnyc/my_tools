// BUDGET5 - Identical to other Budget programs except
//           for the use of an STL list container to
//           hold budget objects (rather than a fixed
//           array or a home made linked list)

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <list>
using namespace std;

// Account - this abstract class incorporates properties
//          common to both account types: Checking and
//          Savings. However, it's missing the concept
//          withdrawal(), which is different between the two
class Account
{
  public:
    Account(unsigned accNo)
    {
      // initialize the data members of the object
      accountNumber = accNo;
      balance = 0;
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
    virtual const char* type() { return "Account"; }

  protected:
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
    Checking(unsigned accNo) :
      Account(accNo)
    { }

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

    Savings(unsigned accNo) : Account(accNo)
    { noWithdrawals = 0; }

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

// AccountPtr - we contain pointers to Account objects
//              and not to objects themselves
typedef Account* AccountPtr;

// prototype declarations
unsigned getAccntNo();
void     process(AccountPtr pAccount);
void     getAccounts(list<AccountPtr>& accList);
void     displayResults(list<AccountPtr>& accList);


// main - accumulate the initial input and output totals
int main(int argcs, char* pArgs[])
{
    // create a link list to attach accounts to
    list<AccountPtr> listAccounts;

    // read accounts from user
    getAccounts(listAccounts);

    // display the linked list of accounts
    displayResults(listAccounts);

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// getAccounts - load up the specified array of Accounts
void getAccounts(list<AccountPtr>& accList)
{
    AccountPtr pA;

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
            pA = new Checking(getAccntNo());
            break;

          case 's':
          case 'S':
            pA = new Savings(getAccntNo());
            break;

          case 'x':
          case 'X':
            return;

          default:
            cout << "I didn't get that.\n";
        }

        // now process the object we just created
        accList.push_back(pA);
        process(pA);
    }
}

// displayResults - display the accounts found in the
//                  Account link list
void displayResults(list<AccountPtr>& accntList)
{
    // now present totals
    double total = 0.0;
    cout << "\nAccount totals:\n";

    // create an iterator and iterate through the list
    // (the type of iter is list<AccountPtr>::iterator
    for (auto iter = accntList.begin();
         iter != accntList.end();
         iter++)
    {
        AccountPtr pAccount = *iter;
        pAccount->display();
        total += pAccount->acntBalance();
    }
    cout << "Total worth = " << total << endl;
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
void process(AccountPtr pAccount)
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
