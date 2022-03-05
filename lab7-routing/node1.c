#include <stdio.h>

extern struct rtpkt
{
	int sourceid;	/* id of sending router sending this pkt */
	int destid;		/* id of router to which pkt being sent
					   (must be an immediate neighbor) */
	int mincost[4]; /* min cost to node 0 ... 3 */
};

extern int TRACE;
extern int YES;
extern int NO;
extern float clocktime;

int connectcosts1[4] = {1, 0, 1, 999};

struct distance_table
{
	int costs[4][4];
} dt1;
void printdt1(struct distance_table *dtptr);
void tolayer2(struct rtpkt packet);
int min();
/* students to write the following two routines, and maybe some others */

void rtinit1()
{
	printf("Initializing node 1 at time %f\n", clocktime);
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			dt1.costs[i][j] = 999;
		}
	}

	dt1.costs[0][1] = 1;
	dt1.costs[0][0] = 1;
	dt1.costs[1][1] = 1;
	dt1.costs[2][1] = 1;
	dt1.costs[2][2] = 1;
	printdt1(&dt1);

	printf("Sending node 1 paths at time %f\n", clocktime);
	struct rtpkt pkt0, pkt2;
	pkt0.sourceid = 1;
	pkt0.destid = 0;
	pkt2.sourceid = 1;
	pkt2.destid = 2;

	for (int i = 0; i < 4; i++)
	{
		pkt0.mincost[i] = dt1.costs[i][1];
		pkt2.mincost[i] = dt1.costs[i][1];
	}
	tolayer2(pkt0);
	tolayer2(pkt2);
}

void rtupdate1(rcvdpkt) struct rtpkt *rcvdpkt;

{
	if (rcvdpkt->destid != 1)
		return;

	int j = rcvdpkt->sourceid;
	int flag = 0;

	printf("\n node 1 recieved packet from %d at time %f \n", j, clocktime);
	for (int i = 0; i < 4; i++)
	{
		if (dt1.costs[i][0] > dt1.costs[j][1] + rcvdpkt->mincost[i])
		{
			dt1.costs[i][0] = dt1.costs[j][1] + rcvdpkt->mincost[i];
			if (i != 0)
			{
				flag = 1;
			}
		}
	}

	if (flag == 1)
	{
		printf("\nDistance table at node 1 updated: \n");
		printdt1(&dt1);

		struct rtpkt pkt0, pkt2;
		pkt0.sourceid = 1;
		pkt0.destid = 0;
		pkt2.sourceid = 1;
		pkt2.destid = 2;
		pkt0.mincost[1] = 0;
		pkt2.mincost[1] = 0;

		for (int i = 0; i < 4; i++)
		{
			if (i == 1)
				continue;
			pkt0.mincost[i] = min(dt1.costs[i][0], dt1.costs[i][2], dt1.costs[i][3]);
			pkt2.mincost[i] = min(dt1.costs[i][0], dt1.costs[i][2], dt1.costs[i][3]);
		}

		printf("\nSending routing packets to nodes 0 and 2 with following mincost vector: \n");
		for (int i = 0; i < 4; i++)
			printf("%d\t", pkt0.mincost[i]);
		printf("\n");
		/*sending dv packets to neighbours*/
		tolayer2(pkt0);
		tolayer2(pkt2);
	}
}

void printdt1(dtptr) struct distance_table *dtptr;

{
	printf("             via   \n");
	printf("   D1 |    0     2 \n");
	printf("  ----|-----------\n");
	printf("     0|  %3d   %3d\n", dtptr->costs[0][0], dtptr->costs[0][2]);
	printf("dest 2|  %3d   %3d\n", dtptr->costs[2][0], dtptr->costs[2][2]);
	printf("     3|  %3d   %3d\n", dtptr->costs[3][0], dtptr->costs[3][2]);
}

linkhandler1(linkid, newcost) int linkid, newcost;
/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */

{
}
