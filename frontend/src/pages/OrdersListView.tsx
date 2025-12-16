import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link } from "react-router-dom";
import { client } from "@/generated-api/client.gen";
import {
  getAllOrdersOrdersGet,
  runPredictionsPredictionsRunPost,
} from "@/generated-api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

// Set base URL for API client
client.setConfig({
  baseUrl: "/backend",
});

export function OrdersListView() {
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const queryClient = useQueryClient();

  const {
    data: orders,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["orders", statusFilter],
    queryFn: () =>
      getAllOrdersOrdersGet({
        query: { status: statusFilter, skip: 0, limit: 100 },
      }),
  });

  const predictMutation = useMutation({
    mutationFn: () => runPredictionsPredictionsRunPost(),
    onSuccess: () => {
      // Refresh orders to show updated predictions
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });

  const handleRunPredictions = () => {
    predictMutation.mutate();
  };

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Error</CardTitle>
          <CardDescription>
            Failed to load orders: {String(error)}
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Customer Orders</h1>
        <div className="flex gap-2">
          <Button
            onClick={handleRunPredictions}
            variant="outline"
            disabled={predictMutation.isPending}
          >
            {predictMutation.isPending ? "Running..." : "Run Predictions"}
          </Button>
          <Link to="/orders/new">
            <Button>Create New Order</Button>
          </Link>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Filter by Status</CardTitle>
          <div className="flex gap-2">
            <Button
              variant={statusFilter === undefined ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter(undefined)}
            >
              All
            </Button>
            <Button
              variant={statusFilter === "pending" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("pending")}
            >
              Pending
            </Button>
            <Button
              variant={statusFilter === "confirmed" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("confirmed")}
            >
              Confirmed
            </Button>
            <Button
              variant={statusFilter === "in_transit" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("in_transit")}
            >
              In Transit
            </Button>
            <Button
              variant={statusFilter === "delivered" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("delivered")}
            >
              Delivered
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="py-8 text-center">Loading orders...</div>
          ) : !orders?.data || orders.data.length === 0 ? (
            <div className="py-8 text-center text-muted-foreground">
              No orders found.{" "}
              <Link to="/orders/new" className="text-primary hover:underline">
                Create one?
              </Link>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order #</TableHead>
                  <TableHead>Customer</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Requested Delivery</TableHead>
                  <TableHead>Predicted Delay (days)</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.data.map((order) => (
                  <TableRow key={order.id}>
                    <TableCell className="font-medium">
                      {order.order_number}
                    </TableCell>
                    <TableCell>{order.customer_name || "-"}</TableCell>
                    <TableCell>
                      <span
                        className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                          order.status === "pending"
                            ? "bg-yellow-100 text-yellow-800"
                            : order.status === "confirmed"
                              ? "bg-blue-100 text-blue-800"
                              : order.status === "in_transit"
                                ? "bg-purple-100 text-purple-800"
                                : order.status === "delivered"
                                  ? "bg-green-100 text-green-800"
                                  : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {order.status}
                      </span>
                    </TableCell>
                    <TableCell>
                      {new Date(
                        order.requested_delivery_date
                      ).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      {order.last_prediction?.predicted_delay_days != null ? (
                        <span
                          className={
                            order.last_prediction.predicted_delay_days > 0
                              ? "font-medium text-red-600"
                              : "text-green-600"
                          }
                        >
                          {order.last_prediction.predicted_delay_days.toFixed(
                            1
                          )}
                        </span>
                      ) : (
                        <span className="text-muted-foreground">N/A</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <Link to={`/orders/${order.id}/recommendations`}>
                        <Button variant="outline" size="sm">
                          View Recommendations
                        </Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
