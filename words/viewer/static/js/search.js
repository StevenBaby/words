$('.ui.search').search({
    apiSettings: {
        url: '/search/{query}',
    },
    fields: {
        // results     : 'words',
        title       : 'title',
        description : "para",
        url         : 'url',
    },
    templates: {
        message: function(message, type) {
            if(message == undefined || type == undefined)
            {
                return html;
            }
            description = '<div class="description">{0}</div class="description">'.format(message);
            header = "";
            if(type == 'empty') {
                header = '<div class="header">{0}</div class="header">'.format(gettext("No Results"))
            }
            return '<div class="message {type}">{0}</div>'.format(header + description);
        }
    },
    error : {
        source      : gettext('Cannot search. No source used, and Semantic API module was not included'),
        noResults   : gettext('Your search returned no results'),
        logging     : gettext('Error in debug logging, exiting.'),
        noEndpoint  : gettext('No search endpoint was specified'),
        noTemplate  : gettext('A valid template name was not specified.'),
        serverError : gettext('There was an issue querying the server.'),
        maxResults  : gettext('Results must be an array to use maxResults setting'),
        method      : gettext('The method you called is not defined.')
    },
});
