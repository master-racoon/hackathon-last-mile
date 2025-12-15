using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;

namespace Seocndry.Common.Helper;

public static class ExpressionHelper
{
    private class ExpressionReplacer(Expression from, Expression to) : ExpressionVisitor
    {
        public override Expression? Visit(Expression? node) => node == from ? to : base.Visit(node);
    }

    public static Expression<Func<TInput, bool>> GetFilter<TInput>(
        string? filter,
        params Expression<Func<TInput, string>>[] fields
    )
    {
        if (string.IsNullOrWhiteSpace(filter))
        {
            return _ => true;
        }

        var words = filter.Split(' ').Select(word => $"%{word}%");

        var tradeParameter = Expression.Parameter(typeof(TInput), "trade");
        var wordExpressions = words
            .Select(word =>
                fields
                    .Select(field =>
                        Expression.Call(
                            null,
                            typeof(NpgsqlDbFunctionsExtensions).GetMethod(
                                nameof(NpgsqlDbFunctionsExtensions.ILike),
                                [typeof(DbFunctions), typeof(string), typeof(string)]
                            ) ?? throw new("ILike method not found"),
                            Expression.Constant(EF.Functions),
                            new ExpressionReplacer(field.Parameters[0], tradeParameter).Visit(field.Body)
                                ?? throw new("Failed to replace parameter"),
                            Expression.Constant(word)
                        ) as Expression
                    )
                    .Aggregate(Expression.OrElse)
            )
            .Aggregate(Expression.AndAlso);

        return Expression.Lambda<Func<TInput, bool>>(wordExpressions, tradeParameter);
    }
}
