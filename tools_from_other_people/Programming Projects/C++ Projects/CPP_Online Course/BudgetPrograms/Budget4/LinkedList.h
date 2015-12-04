// AccountLinkedList - maintain a linked list of Account
//                     objects

#ifndef _ACCOUNTLINKEDLIST_
#define _ACCOUNTLINKEDLIST_

// declare base linked list in advance
template <class T> class LinkedList;

// Node - a node within a linked list; each Node points
//        to an Account object
template <class T> class Node
{
    public:
        Node(LinkedList<T>* pL, T* pT)
        {
            pList = pL;
            pNext = 0;
            pObject = pT;
        }

        Node<T>* next() { return pNext; }
        Node<T>* next(Node<T>* pN) { pNext = pN; return pNext; }
        T* current() { return pObject; }

    protected:
        LinkedList<T>* pList;
        Node<T>* pNext;
        T* pObject;
};

// LinkedList - represents LinkedList of Node objects
template <class T> class LinkedList
{
    public:
        LinkedList<T>() { pFirst = 0; }
        Node<T>* firstNode() { return pFirst; }
        Node<T>* lastNode()
        {
            // if the list is empty just return a null
            if (pFirst == 0)
            {
                return 0;   // empty list; make it first
            }

            // else search for the last element in the list
            Node<T>* pN = pFirst;
            while(true)
            {
                Node<T>* pNext = pN->next();
                if (pNext == 0)
                {
                    break;
                }
                pN = pNext;
            }
            return pN;
        }

        void  addNode(Node<T>* pNode)
        {
            Node<T>* pN = lastNode();
            if (pN == 0)
            {
                pFirst = pNode;
            }
            else
            {
                pN->next(pNode);
            }
        }

    protected:
        Node<T>* pFirst;
};

#endif

