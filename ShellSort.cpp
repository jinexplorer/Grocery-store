void ShellSort(int R[],int n)
{
	int tmp;
	int d=n/2;
	while(d>=1)
	{
		int j=0;
		for(int i=d;i<n;i++)
		{
			tmp=R[i];
			j=i-d;
			while(j>=0&&tmp<R[j])
			{
				R[j+d]=R[j];
				j-=d;
			}
			R[j+d]=tmp;
		}
		d/=2;	
	}
}
