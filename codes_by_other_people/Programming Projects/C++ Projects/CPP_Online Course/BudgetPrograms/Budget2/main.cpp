//
// BUDGET - Budget program with active Savings and
//          Checking classes.
//
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// the maximum number of accounts one can have
const int MAXACCOUNTS = 10;

// Checking - this describes checking accounts
class Checking
{
  public:
    Checking(int initializeAN = 0)
         : accountNumber(initializeAN), balance(0.0) {}

    // access functions
    int accountNo() { return accountNumber; }
    double acntBalance() { return balance; }

    // transaction functions
    double deposit(double amount)
    {
        balance += amount;
        return balance;
    }
    double withdrawal(double amount);

    // display function for displaying self on 'cout'
    void display()
    {
        cout << "Account " << accountNumber
             << " = "   << balance
             << endl;
    }

  protected:
    unsigned accountNumber;
    double  balance;
};
//
// withdrawal - this member function is too big to
//              be defined inline
double Checking::withdrawal(double amount)
{
    if (balance < amount)
    {
        cout << "Insufficient funds: balance " << balance
             << ", check "           << amount
             << endl;
        return false;
    }
    else
    {
        balance -= amount;

        // if balance falls too low,...
        if (balance < 500.00)
        {
            // ...charge a service fee
            balance -= 0.20;
        }
    }
    return true;
}

// Savings - you can probably figure this one out
class Savings
{
  public:
    Savings(int initialAN = 0)
         : accountNumber(initialAN),
         balance(0.0), noWithdrawals(0) {}

    // access functions
    int accountNo() { return accountNumber; }
    double acntBalance() { return balance; }

    // transaction functions
    double deposit(double amount)
    {
        balance += amount;
        return balance;
    }
    bool withdrawal(double amount);

    // display function - display self to cout
    void display()
    {
        cout << "Account "           << accountNumber
             << " = "                  << balance
             << " (no. withdrawals = " << noWithdrawals
             << ")" << endl;
    }
  protected:
    unsigned accountNumber;
    double  balance;
    int   noWithdrawals;
};
bool Savings::withdrawal(double amount)
{
    if (balance < amount)
    {
        cout << "Insufficient funds: balance " << balance
             << ", withdrawal "        << amount
             << endl;
        return false;
    }
    else
    {
        // after more than one withdrawal in a month...
        if (++noWithdrawals > 1)
        {
            // ...charge a $5 fee
            balance -= 5.00;
        }

        // now make the withdrawal
        balance -= amount;
    }
    return true;
}

// prototype declarations
void process(Checking* pChecking);
void process(Savings*  pSavings);

// checking and savings account objects
Checking* chkAcnts[MAXACCOUNTS];
Savings*  svgAcnts[MAXACCOUNTS];

// main - accumulate the initial input and output totals
int main(int argcs, char* pArgs[])
{
    // loop until someone enters an 'X' or 'x'
    int noChkAccounts = 0;  // count the number of accounts
    int noSvgAccounts = 0;
    char   accountType;   // S or C
    while(true)
    {
        cout << "Enter S for Savings, "
             << "C for Checking, "
             << "X for exit:";
        cin >> accountType;

        // exit the loop when the user enters an X
        if (accountType == 'x' || accountType == 'X')
        {
            break;
        }

        // otherwise, handle according to the account type
        switch (accountType)
        {
          // checking account
          case 'c':
          case 'C':
            if (noChkAccounts < MAXACCOUNTS)
            {
                int acnt;
                cout << "Enter account number:";
                cin  >> acnt;
                chkAcnts[noChkAccounts] =
                                     new Checking(acnt);
                process(chkAcnts[noChkAccounts]);
                noChkAccounts++;
            }
            else
            {
                cout << "No more room for checking accounts"
                     << endl;
            }
            break;

          // savings account
          case 's':
          case 'S':
            if (noSvgAccounts < MAXACCOUNTS)
            {
                int acnt;
                cout << "Enter account number:";
                cin  >> acnt;
                svgAcnts[noSvgAccounts] = new Savings(acnt);
                process(svgAcnts[noSvgAccounts]);
                noSvgAccounts++;
            }
            else
            {
                cout << "No more room for savings accounts"
                     << endl;
            }
            break;

          default:
            cout << "I didn't get that." << endl;
      }
    }

    // now present totals
    double chkTotal = 0;    // total of all checking accounts
    cout << "Checking accounts:\n";
    for (int i = 0; i < noChkAccounts; i++)
    {
        chkAcnts[i]->display();
        chkTotal += chkAcnts[i]->acntBalance();
    }

    double svgTotal = 0;    // total of all savings accounts
    cout << "Savings accounts:\n";
    for (int j = 0; j < noSvgAccounts; j++)
    {
        svgAcnts[j]->display();
        svgTotal += svgAcnts[j]->acntBalance();
    }

    double total = chkTotal + svgTotal;
    cout << "Total for checking accounts = "
         << chkTotal
         << endl;

    cout << "Total for savings accounts = "
         << svgTotal
         << endl;

    cout << "Total worth         = "
         << total
         << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// process(Checking) - input the data for a checking account
void process(Checking* pChecking)
{
    cout << "Enter positive number for deposit,\n"
         << "negative for check, 0 to terminate"
         << endl;
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
          pChecking->deposit(transaction);
        }

        // withdrawal
        if (transaction < 0)
        {
          pChecking->withdrawal(-transaction);
        }
    }
}

// process(Savings) - input the data for a savings account
void process(Savings* pSavings)
{
    cout << "Enter positive number for deposit,\n"
         << "negative for withdrawal, 0 to terminate"
         << endl;
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
          pSavings->deposit(transaction);
        }

        // withdrawal
        if (transaction < 0)
        {
          pSavings->withdrawal(-transaction);
        }
    }
}
