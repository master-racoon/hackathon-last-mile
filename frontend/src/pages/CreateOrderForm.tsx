import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  createOrderOrdersPost,
} from "@/generated-api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function CreateOrderForm() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: vehicleTypes } = useQuery({
    queryKey: ["vehicleTypes"],
    queryFn: () => getAllVehicleTypesVehicleTypesGet(),
  });

  const [formData, setFormData] = useState({
    order_number: "",
    customer_name: "",
    requested_delivery_date: "",
    vehicle_type_id: "",
    lead_time_days: "",
    load_date: "",
    estimated_arrival: "",
    origin_state: "",
    origin_country: "",
    destination_state: "",
    destination_country: "",
    gross_weight_kg: "",
    net_weight_kg: "",
    total_width: "",
    line_item_count: "",
    delivery_method: "",
    notes: "",
    status: "pending",
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => createOrderOrdersPost({ body: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
      navigate("/");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Transform form data to match API schema
    const payload: any = {
      order_number: formData.order_number,
      customer_name: formData.customer_name || null,
      requested_delivery_date: formData.requested_delivery_date,
      vehicle_type_id: formData.vehicle_type_id
        ? parseInt(formData.vehicle_type_id)
        : null,
      lead_time_days: formData.lead_time_days
        ? parseInt(formData.lead_time_days)
        : null,
      load_date: formData.load_date || null,
      estimated_arrival: formData.estimated_arrival || null,
      origin_state: formData.origin_state || null,
      origin_country: formData.origin_country || null,
      destination_state: formData.destination_state || null,
      destination_country: formData.destination_country || null,
      gross_weight_kg: formData.gross_weight_kg
        ? parseFloat(formData.gross_weight_kg)
        : null,
      net_weight_kg: formData.net_weight_kg
        ? parseFloat(formData.net_weight_kg)
        : null,
      total_width: formData.total_width
        ? parseFloat(formData.total_width)
        : null,
      line_item_count: formData.line_item_count
        ? parseInt(formData.line_item_count)
        : null,
      delivery_method: formData.delivery_method
        ? parseInt(formData.delivery_method)
        : null,
      notes: formData.notes || null,
      status: formData.status,
    };

    createMutation.mutate(payload);
  };

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Create Customer Order</h1>
        <Button variant="outline" onClick={() => navigate("/")}>
          Cancel
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Order Details</CardTitle>
          <CardDescription>
            Fill in the details for the new customer order
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Information */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="order_number">Order Number *</Label>
                <Input
                  id="order_number"
                  name="order_number"
                  value={formData.order_number}
                  onChange={handleChange}
                  required
                  placeholder="ORD-001"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="customer_name">Customer Name</Label>
                <Input
                  id="customer_name"
                  name="customer_name"
                  value={formData.customer_name}
                  onChange={handleChange}
                  placeholder="Acme Corp"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="line_item_count">Line Item Count</Label>
                <Input
                  id="line_item_count"
                  name="line_item_count"
                  type="number"
                  value={formData.line_item_count}
                  onChange={handleChange}
                  placeholder="1"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="delivery_method">Delivery Method</Label>
                <Input
                  id="delivery_method"
                  name="delivery_method"
                  type="number"
                  value={formData.delivery_method}
                  onChange={handleChange}
                  placeholder="1"
                />
              </div>
            </div>

            {/* Dates */}
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="requested_delivery_date">
                  Requested Delivery Date *
                </Label>
                <Input
                  id="requested_delivery_date"
                  name="requested_delivery_date"
                  type="date"
                  value={formData.requested_delivery_date}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="load_date">Load Date</Label>
                <Input
                  id="load_date"
                  name="load_date"
                  type="date"
                  value={formData.load_date}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="estimated_arrival">Estimated Arrival</Label>
                <Input
                  id="estimated_arrival"
                  name="estimated_arrival"
                  type="date"
                  value={formData.estimated_arrival}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* Shipping Details */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="vehicle_type_id">Vehicle Type</Label>
                <select
                  id="vehicle_type_id"
                  name="vehicle_type_id"
                  value={formData.vehicle_type_id}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <option value="">Select vehicle type</option>
                  {vehicleTypes?.data?.map((vt: any) => (
                    <option key={vt.id} value={vt.id}>
                      {vt.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="lead_time_days">Lead Time (days)</Label>
                <Input
                  id="lead_time_days"
                  name="lead_time_days"
                  type="number"
                  value={formData.lead_time_days}
                  onChange={handleChange}
                  placeholder="7"
                />
              </div>
            </div>

            {/* Origin and Destination */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="origin_state">Origin State/City</Label>
                <Input
                  id="origin_state"
                  name="origin_state"
                  value={formData.origin_state}
                  onChange={handleChange}
                  placeholder="Western Cape"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="origin_country">Origin Country</Label>
                <Input
                  id="origin_country"
                  name="origin_country"
                  value={formData.origin_country}
                  onChange={handleChange}
                  placeholder="South Africa"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="destination_state">
                  Destination State/City
                </Label>
                <Input
                  id="destination_state"
                  name="destination_state"
                  value={formData.destination_state}
                  onChange={handleChange}
                  placeholder="Gauteng"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="destination_country">Destination Country</Label>
                <Input
                  id="destination_country"
                  name="destination_country"
                  value={formData.destination_country}
                  onChange={handleChange}
                  placeholder="South Africa"
                />
              </div>
            </div>

            {/* Cargo Details */}
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="gross_weight_kg">Gross Weight (kg)</Label>
                <Input
                  id="gross_weight_kg"
                  name="gross_weight_kg"
                  type="number"
                  step="0.01"
                  value={formData.gross_weight_kg}
                  onChange={handleChange}
                  placeholder="1000.50"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="net_weight_kg">Net Weight (kg)</Label>
                <Input
                  id="net_weight_kg"
                  name="net_weight_kg"
                  type="number"
                  step="0.01"
                  value={formData.net_weight_kg}
                  onChange={handleChange}
                  placeholder="950.00"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="total_width">Total Width</Label>
                <Input
                  id="total_width"
                  name="total_width"
                  type="number"
                  step="0.01"
                  value={formData.total_width}
                  onChange={handleChange}
                  placeholder="2.4"
                />
              </div>
            </div>

            {/* Status and Notes */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="in_transit">In Transit</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Notes</Label>
              <textarea
                id="notes"
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Additional notes..."
              />
            </div>

            <div className="flex gap-4">
              <Button type="submit" disabled={createMutation.isPending}>
                {createMutation.isPending ? "Creating..." : "Create Order"}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/")}
              >
                Cancel
              </Button>
            </div>

            {createMutation.isError && (
              <div className="text-destructive text-sm">
                Error creating order: {String(createMutation.error)}
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
