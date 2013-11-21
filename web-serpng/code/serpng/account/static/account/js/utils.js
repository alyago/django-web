function ValidateEmail(email) {

    // Trim leading and trailing whitespace.
    //
    if (email.replace) {
        email = email.replace(/(^\s+|\s+$)/g, '');
    }

    if (email == '') {
        throw {
            name: 'BlankEmailException',
            message: 'Please enter your email address.'
        }
    } else if (email.match(/^[^@\s]+@[^@\.\s]+\.[^@\s]*[^.]$/) == null) {
        throw {
            name: 'InvalidEmailException',
            message: 'Please enter a valid email address.'
        }
    }
}

function MakeUri(path, queryParamDict) {
    var uri = path;

    var queryParamsList = [];
    for (var queryKey in queryParamDict) {
        var queryValue = queryParamDict[queryKey];
        if (typeof(queryValue) != 'undefined' && queryValue != '') {
            queryParamsList.push(queryKey + '=' + encodeURIComponent(queryValue));
        }
    }

    if (queryParamsList.length > 0) {
        uri += '?' + queryParamsList.join('&');
    }

    return uri;
}
