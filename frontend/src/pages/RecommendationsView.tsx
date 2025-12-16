import { useQuery } from "@tanstack/react-query";
import { useParams, Link } from "react-router-dom";
import {
  getOrderOrdersOrderIdGet,
  getOrderRecommendationsOrdersOrderIdRecommendationsGet,
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

export function RecommendationsView() {
  const { orderId } = useParams<{ orderId: string }>();

  const { data: order, isLoading: orderLoading } = useQuery({
    queryKey: ["order", orderId],
    queryFn: () =>
      getOrderOrdersOrderIdGet({ path: { order_id: parseInt(orderId!) } }),
    enabled: !!orderId,
  });

  const { data: recommendations, isLoading: recsLoading } = useQuery({
    queryKey: ["recommendations", orderId],
    queryFn: () =>
      getOrderRecommendationsOrdersOrderIdRecommendationsGet({
        path: { order_id: parseInt(orderId!) },
      }),
    enabled: !!orderId,
  });

  if (orderLoading || recsLoading) {
    return (
      <Card>
        <CardContent className="py-8 text-center">Loading...</CardContent>
      </Card>
    );
  }

  if (!order?.data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Order Not Found</CardTitle>
          <CardDescription>
            The requested order could not be found.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Link to="/">
            <Button>Back to Orders</Button>
          </Link>
        </CardContent>
      </Card>
    );
  }

  const orderData = order.data;
  const recsList = (recommendations?.data || []) as any[];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Order Recommendations</h1>
        <Link to="/">
          <Button variant="outline">Back to Orders</Button>
        </Link>
      </div>

      {/* Order Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Order: {orderData.order_number}</CardTitle>
          <CardDescription>
            Customer: {orderData.customer_name || "N/A"} | Status:{" "}
            {orderData.status}
          </CardDescription>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Requested Delivery
            </div>
            <div className="text-lg">
              {new Date(orderData.requested_delivery_date).toLocaleDateString()}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Load Date
            </div>
            <div className="text-lg">
              {orderData.load_date
                ? new Date(orderData.load_date).toLocaleDateString()
                : "N/A"}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Origin
            </div>
            <div className="text-lg">
              {orderData.origin_city || "N/A"},{" "}
              {orderData.origin_country || "N/A"}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Destination
            </div>
            <div className="text-lg">
              {orderData.destination_city || "N/A"},{" "}
              {orderData.destination_country || "N/A"}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Weight
            </div>
            <div className="text-lg">
              {orderData.weight_kg ? `${orderData.weight_kg} kg` : "N/A"}
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground">
              Volume
            </div>
            <div className="text-lg">
              {orderData.volume_m3 ? `${orderData.volume_m3} m³` : "N/A"}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Predictions/Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>Prediction History</CardTitle>
          <CardDescription>
            All predictions generated for this order
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!recsList || recsList.length === 0 ? (
            <div className="py-8 text-center text-muted-foreground">
              No predictions available yet. Run predictions from the orders list
              to generate them.
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Prediction Date</TableHead>
                  <TableHead>Predicted Delay (days)</TableHead>
                  <TableHead>Recommended Vehicle Type ID</TableHead>
                  <TableHead>Confidence</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recsList.map((rec: any) => (
                  <TableRow key={rec.id}>
                    <TableCell>
                      {new Date(rec.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <span
                        className={
                          rec.predicted_delay_days > 0
                            ? "font-medium text-red-600"
                            : "text-green-600"
                        }
                      >
                        {rec.predicted_delay_days?.toFixed(2) ?? "N/A"}
                      </span>
                    </TableCell>
                    <TableCell>
                      {rec.recommended_vehicle_type_id || "N/A"}
                    </TableCell>
                    <TableCell>
                      {rec.confidence
                        ? `${(rec.confidence * 100).toFixed(1)}%`
                        : "N/A"}
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
