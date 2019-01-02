#include<stdio.h>
#include<stdlib.h>

#define Maxlength 50
#define Maxtree 50

typedef char ElemType;

typedef struct tnode
{
	ElemType data;
	struct tnode *hp;//指向同行结点 
	struct tnode *vp;//指向子结点 
}TSBNode;

void start(void);
void CreatTree(TSBNode *&a,ElemType str[],int &strnum);
void GetTree(TSBNode *a,ElemType str[Maxtree][2*Maxtree],int length);
char MaxLength(ElemType str[Maxtree][2*Maxtree],int length);
void display(ElemType str[Maxtree][2*Maxtree]);
void DestoryTree(TSBNode *&a);

int main()
{
	start();
	return 0;
}

//开始程序，进入一个可以重复运行的循环 
void start(void)
{
	int choice=0;
	do{
		//清屏 
		system("cls");
		//创建一个指向树的指针 
		TSBNode *a=NULL;
		//获得用户输入的字符串 
		ElemType str[Maxlength];
		puts("请输入创建树所用的字符串!");
		scanf("%s",str);
		//进行树的创造 
		int strnum=0;
		CreatTree(a,str,strnum);
		//获得数的结构并打印出数的整个结构 
		ElemType str1[Maxtree][2*Maxtree]={'\0'}; 
		GetTree(a,str1,0);
		display(str1);
		
		//显示出交互的提示性语句 
		puts("\n\n\n\n\n\n\n\n\n-------------------------------------------------");
		puts("再来一次  1\t结束程序  others");
		scanf("%d",&choice);
		DestoryTree(a); 
	}while(choice==1);
	
} 


//以孩子兄弟链的方式创建一棵树 
void CreatTree(TSBNode *&a,ElemType str[],int &strnum)
{
	//strnum代表当前读取的字符的位置 
	//采用尾插法 
	TSBNode *p=a,*tail=a;
	//读取字符串 
	char ch;
	ch=str[strnum++];
	while(ch!='\0')
	{
		if(ch==')')
			break;
			//直接返回 
		else if(ch=='(')
			CreatTree(p->vp,str,strnum);
		//进行递归调用 
		else if(ch==',');//什么也不做 
		else
		{
			//创建一个新的结点，尾插法 
			p=(TSBNode *)malloc(sizeof(TSBNode));
			p->hp=p->vp=NULL;
			p->data=ch;
			if(tail==NULL)
				a=p;
			else
				tail->hp=p;
			tail=p;		
		}
		ch=str[strnum++];		 
	}
}


//遍历整个树，然后将整个树的结构存储到一个数组中
//数组的第一列单独出现，用来存储这个树的这一高度的最右边的位置 
void GetTree(TSBNode *a,ElemType str[Maxtree][2*Maxtree],int length)
{
	//str用来存放树形	length代表当前树的高度 
	TSBNode *p=a;
	int flag=0;//用来指示前一个结点是否存在孩子结点
	//代表调用函数的第一个结点
	str[length][0]++;
	str[length][str[length][0]]='{';
	str[length][0]++;
	str[length][str[length][0]]=p->data;
	//判断其是否存在孩子结点，如果存在则递归调用 
	if(p->vp!=NULL)
		{
			str[length+1][0]=str[length][0]-2;	
			//根据自身算法特点，向后移动两位正好存储{和结点数据，使得上下对齐 
			GetTree(p->vp,str,length+1);
			//代表有孩子结点 
			flag=1;
		}
		
	p=p->hp;
	//判断是否有兄弟结点 
	while(p!=NULL)
	{
		if(flag==1)
		{
			if(p->vp!=NULL)
			{
				//前一个兄弟结点存在孩子结点并且本节点存在孩子结点
	//找到此节点后面结点的最大值，之后将本节点进行偏移，偏移之后使孩子结点的{和结点值与自己对齐 
				str[length][0]=MaxLength(str,length+1)+2;
				str[length][str[length][0]]=p->data;
				str[length+1][0]=str[length][0]-2;
				GetTree(p->vp,str,length+1);
				//关键更改 
				flag=1;
			}
			else
			{
				//前一个兄弟结点存在孩子结点并且本节点存在孩子结点
				//此种不需要考虑孩子结点的{的情况，所以只需偏移1个单位即可 
				str[length][0]=MaxLength(str,length+1)+1;
				str[length][str[length][0]]=p->data;
				//关键更改 
				flag=0;
			}
		}
		else
		{
			if(p->vp!=NULL)
			{
				//前一个兄弟结点不存在孩子结点并且本节点存在孩子结点
		//此种情况无法通过后序层数的最大值进行偏移，但直接可以在本行进行偏移 ，偏移为2，考虑{ 
				str[length][0]+=2;
				str[length][str[length][0]]=p->data;
				str[length+1][0]=str[length][0]-2;
				GetTree(p->vp,str,length+1);
				//关键更改 
				flag=1;
			}
			else
			{
				//前一个兄弟结点不存在孩子结点并且本节点不存在孩子结点
		//此种情况无法通过后序层数的最大值进行偏移，但直接可以在本行进行偏移 ，偏移为1
				str[length][0]+=1;
				str[length][str[length][0]]=p->data;
				//关键更改 
				flag=0;
			}
		}
		
		p=p->hp;
	} 
	//调用返回的输出符号 
	str[length][0]++;
	str[length][str[length][0]]='}';
}

//得到此树的这一层与之后的层数中最长的那一层的长度 
ElemType MaxLength(ElemType str[Maxtree][2*Maxtree],int length)
{
	ElemType ret=str[length][0];
	while(str[length][0] != '\0')
	{
		if(str[length][0]>ret)
			ret=str[length][0];
		length++;
	}
	return ret;
}

//将得到的数组打印出来，忽略第一列 
void display(ElemType str[Maxtree][2*Maxtree])
{
	for(int i=0;str[i][0]!='\0';i++)
	{
		for(int j=1;j<=str[i][0];j++)
		{
			printf("%-2c",str[i][j]);
		}
		printf("\n");
	}
}


void DestoryTree(TSBNode *&a)
{
	TSBNode *p=a;
	//有儿子先去消灭儿子 
	if(p->vp!=NULL)
		DestoryTree(p->vp);
	//儿子没了，灭兄弟 
	if(p->hp!=NULL)
		DestoryTree(p->hp);
	//灭了 
	free(p);
} 
