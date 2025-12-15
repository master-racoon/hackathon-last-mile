using LastMile.Common.Exceptions;
using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

namespace LastMile.Common.Extensions;

public static class QueryableExtensions
{
    public static async Task<T> FirstOrThrowAsync<T>(
        this IQueryable<T> query,
        Expression<Func<T, bool>> predicate) where T : class
    {
        var result = await query.FirstOrDefaultAsync(predicate);
        if (result == null)
        {
            throw new ObjectNotFoundException($"{typeof(T).Name} not found");
        }
        return result;
    }
}
