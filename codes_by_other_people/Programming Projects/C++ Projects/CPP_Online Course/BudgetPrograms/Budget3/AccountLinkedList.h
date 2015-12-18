// AccountLinkedList - maintain a linked list of Account
//                     objects

#ifndef _ACCOUNTLINKEDLIST_
#define _ACCOUNTLINKEDLIST_

// this unfortunate declaration results from the fact that
// Account is not part of the Lists namespace. This problem
// goes away in the next version, Budget4 in Part V.
class Account;
namespace Lists
{

    // declare classes in advance
    class AccountLinkedList;
    class Node;

    // LinkedList - represents LinkedList of Node objects
    class AccountLinkedList
    {
        public:
          AccountLinkedList() { pHead = 0; }
          void  addNode(Node* pNode);
          Node* firstNode() { return pHead; }

        protected:
          Node* pHead;
    };

    // Node - a node within a linked list; each Node points
    //        to an Account object
    class Node
    {
        friend class AccountLinkedList;
      public:
        Node(AccountLinkedList* pL, Account* pAcc)
        {
            pList = pL;
            pNext = 0;
            pAccount = pAcc;

            pL->addNode(this);
        }
        static Node* firstNode(AccountLinkedList* pList)
        {
            return pList->firstNode();
        }

        Node* nextNode() { return pNext; }
        Account* currentAccount() { return pAccount; }

      protected:
        AccountLinkedList* pList;
        Node* pNext;
        Account* pAccount;
    };
}
#endif
