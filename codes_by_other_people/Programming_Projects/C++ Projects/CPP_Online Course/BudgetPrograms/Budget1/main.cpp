// BUDGET1 - A "functional" Budget program;
//           this program accepts deposits and
//           withdrawals on some number of accounts;
//           eventually it displays the accounts
//           created
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

// the maximum number of accounts you can have
const int maxAccounts = 10;

// data describes accounts
unsigned accountNumber[maxAccounts];
double   balance[maxAccounts];


// prototype declarations
void process(unsigned accountNumber,
             double*  pBalance);
void init(unsigned* pAccountNumber,
          double*   pBalance);

// main - accumulate the initial input and output totals
int main(int nNumberofArgs, char* pszArgs[])
{
   cout << "Enter C to continue or X to terminate:";
   // loop until someone enters
   int noAccounts = 0;         // the number of accounts

   // don't create more accounts than we have room for
   cout << "This program creates bank accounts\n" << endl;
   while (noAccounts < maxAccounts)
   {
       char transactionType;
       cout << "Enter C to create another account"
            << " or X to terminate:";
       cin  >> transactionType;

       // quit if the user enters an X; otherwise...
       if (transactionType == 'x' ||
           transactionType == 'X')
       {
           break;
       }

       // if the user enters a C then...
       if (transactionType == 'c' ||
           transactionType == 'C')
       {
          // initialize a new account...
          // (pass address so that function can change
          // the value for us)
          init(&accountNumber[noAccounts],
               &balance[noAccounts]);

          // input transaction information
          process(accountNumber[noAccounts],
                  &balance[noAccounts]);

          // move the index over to the next account
          noAccounts++;
       }
   }

   // now present totals
   // first for each account
   double total = 0;
   cout << "Account information:\n";
   for (int i = 0; i < noAccounts; i++)
   {
      cout << "Balance for account "
           << accountNumber[i]
           << " = "
           << balance[i]
           << endl;

      // accumulate the total for all accounts
      total += balance[i];
   }


   // now display the accumulated value
   cout << "Balance for all accounts = " << total << endl;

    // wait until user is ready before terminating program
    // to allow the user to see the program results
    system("PAUSE");
    return 0;
}

// init - initialize an account by reading
//        in the account number and zeroing out the
//        balance (use pointers now)
void init(unsigned* pAccountNumber,
          double*   pBalance)
{
   cout << "Enter account number:";
   cin  >> *pAccountNumber;
   *pBalance = 0.0;
}

// process - update the account balance by entering
//           the transactions from the user
//           (use a reference argument for this example -
//           the effect is the same as using a pionter)
void process(unsigned accountNumber,
             double*  pBalance)
{
   cout << "Enter positive number for deposit,\n"
        << "negative for withdrawal,\n"
        << " or zero to terminate"
        << endl;

   double transaction;
   while(true)
   {
      cout << ":";
      cin  >> transaction;

      // exit if transaction is zero
      if (transaction == 0)
      {
          break;
      }

      // if it's a deposit...
      if (transaction > 0)
      {
         // ...add it to the balance
         *pBalance += transaction;
      }

      // ...otherwise, it must be a withdrawal
      else
      {
         // withdrawal - it's easier
         // to think of a withdrawal as a positive number
         transaction = -transaction;
         if (*pBalance < transaction)
         {
            cout << "Insufficient funds: balance "
                 << *pBalance
                 << ", check "
                 << transaction
                 << "\n";
         }
         else
         {
            *pBalance -= transaction;
         }
      }
   }
}

