using System.Data;
using System.Transactions;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using LastMile.Common.Exceptions;

namespace LastMile.Controllers;

/// <summary>
/// Represents an API controller that handles application errors.
/// </summary>
[ApiExplorerSettings(IgnoreApi = true)]
[ApiController]
public class ErrorController : ControllerBase
{
    /// <summary>
    /// Handles exceptions thrown in the application, returns HTTP response with relevant information.
    /// </summary>
    /// <returns>Problem details containing the exception information.</returns>
    [Route("error")]
    public ActionResult<ProblemDetails> Error()
    {
        var context = HttpContext.Features.Get<IExceptionHandlerPathFeature>();
        var exception = context?.Error;
        var path = context?.Path;
        if (exception == null)
            return StatusCode(500);

        var problemDetails = new ApiExceptionDetails { Instance = path };

        var code = 500; // Internal Server Error by default
        ApiErrorCode? errorCode = null;
        string? type = null;
        string? title = null;

        // Each case of the switch statement handles a specific type of exception.
        // Additional details can be found in the specific exception documentation.
        switch (exception)
        {
            case ApiException apiException:
                errorCode = apiException.ErrorCode;
                type = apiException.ErrorCode.ToString();
                code = 400; // Bad Request
                break;
            case AuthException:
                type = "authentication_error";
                code = 401; // Unauthorized
                title = exception.Message;
                break;
            case TermsException:
                type = "terms_error";
                code = 403; // Forbidden
                title = exception.Message;
                break;
            case InvalidOperationException:
                type = "invalid_operation";
                code = 403; // Forbidden
                title = exception.Message;
                break;
            case ConstraintException:
                type = "constraint_violation";
                code = 403; // Forbidden
                title = exception.Message;
                break;
            case ArgumentOutOfRangeException:
                type = "argument_out_of_range";
                code = 400; // Bad Request
                title = exception.Message;
                break;
            case ArgumentException:
                type = "illegal_argument";
                code = 400; // Bad Request
                title = exception.Message;
                break;
            case DuplicateNameException:
                type = "duplicate_name";
                code = 400; // Bad Request
                title = exception.Message;
                break;

            case DbUpdateConcurrencyException:
                title = "database_concurrency_error";
                code = 500;
                break;
            case DbUpdateException:
                title = "Database exception";
                code = 500; // Internal server error. Often these errors could be things like bad requests caused by "concurrency" issues
                break;
            case TransactionAbortedException:
                title = "Transaction exception";
                code = 500; // Internal server error. Often these errors could be things like bad requests caused by "concurrency" issues
                break;
        }

        problemDetails.ErrorCode = errorCode;
        problemDetails.Type = type;
        problemDetails.Status = code;
        problemDetails.Title = title;
        return problemDetails;
    }
}
