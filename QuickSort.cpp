int partition(int R[],int i,int j)
{
	int tmp=R[i];
	while(i<j)
	{
		while(j>i&&R[j]>=tmp)
			j--;
		R[i]=R[j];
		while(i<j&&R[i]<=tmp)
			i++;
		R[j]=R[i];
	}
	R[i]=tmp;
	return i;
 } 
 void QuickSort(int R[],int i,int j)
 {
 	if(i<j)
 	{
 		int k=partition(R,i,j);
 		QuickSort(R,i,k-1);
 		QuickSort(R,k+1,j);
	 }
 }
