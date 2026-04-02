using System;
using System.Collections.Generic;
using System.Linq;

public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
}

public class Order
{
    public int OrderId { get; set; }
    public int CustomerId { get; set; }
    public decimal Amount { get; set; }
}

public static class InputScenario
{
    public static List<string> BuildHighValueCustomerNames(
        List<Customer> customers,
        List<Order> orders,
        decimal threshold)
    {
        var results = new List<string>();

        // Intentional O(n^2): nested scans to give analyzer something to flag.
        foreach (var customer in customers)
        {
            decimal total = 0;
            foreach (var order in orders)
            {
                if (order.CustomerId == customer.Id)
                {
                    total += order.Amount;
                }
            }

            if (total > threshold)
            {
                results.Add(customer.Name);
            }
        }

        return results;
    }

    public static int CountLargeOrdersSlow(List<Order> orders, decimal minAmount)
    {
        int count = 0;

        // Intentional repeated Count() and ElementAt() usage over IEnumerable.
        IEnumerable<Order> query = orders.Where(o => o.Amount > 0);
        for (int i = 0; i < query.Count(); i++)
        {
            if (query.ElementAt(i).Amount >= minAmount)
            {
                count++;
            }
        }

        return count;
    }

    public static void Main()
    {
        var customers = new List<Customer>
        {
            new Customer { Id = 1, Name = "Ada" },
            new Customer { Id = 2, Name = "Linus" },
            new Customer { Id = 3, Name = "Grace" }
        };

        var orders = new List<Order>
        {
            new Order { OrderId = 100, CustomerId = 1, Amount = 120 },
            new Order { OrderId = 101, CustomerId = 1, Amount = 80 },
            new Order { OrderId = 102, CustomerId = 2, Amount = 40 },
            new Order { OrderId = 103, CustomerId = 3, Amount = 300 },
            new Order { OrderId = 104, CustomerId = 3, Amount = 25 }
        };

        var names = BuildHighValueCustomerNames(customers, orders, 150);
        Console.WriteLine(string.Join(", ", names));

        var count = CountLargeOrdersSlow(orders, 50);
        Console.WriteLine($"Large order count: {count}");
    }
}
