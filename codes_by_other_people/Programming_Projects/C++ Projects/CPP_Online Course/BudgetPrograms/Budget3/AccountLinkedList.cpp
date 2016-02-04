// AccountLinkedList - maintain a linked list of Account
//                     objects
#include "AccountLinkedList.h"

namespace Lists
{
    // addNode -add a node at the beginning of the current
    //          linked list
    void  AccountLinkedList::addNode(Node* pNode)
    {
        pNode->pNext = pHead;
        pHead = pNode;
    }
}
