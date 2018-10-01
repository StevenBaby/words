$.fn.form.settings.rules.not_number = function(value) {
    return ! /^\d+$/.test(value);
};

var validates = {
    username: {
        identifier  : 'username',
        rules: [{
                type   : 'minLength[2]',
                prompt : gettext('Please enter username at least 2 character')
                },
                {
                type   : 'maxLength[32]',
                prompt : gettext('Please enter username at most 32 character')
                }]
    },
    email: {
        identifier  : 'email',
        rules: [{
                type   : 'email',
                prompt : gettext('Please enter valid email')
        }]
    },
    password: {
        identifier  : 'password',
        rules: [{
            type   : 'empty',
            prompt : gettext('Please enter your password')
        }]
    },

    captcha: {
        identifier  : 'captcha_1',
        rules: [{
            type   : 'exactLength[4]',
            prompt : gettext('Please enter captcha 4 character')
        }]
    },

    password1: {
        identifier  : 'password1',
        rules: [
        {
            type   : 'minLength[8]',
            prompt : gettext('Please enter password at least 8 character')
        },
        {
            type   : 'not_number',
            prompt : gettext('Password cannot be all number')
        }
        ]
    },
    password2: {
        identifier  : 'password2',
        rules: [{
            type   : 'match[password1]',
            prompt : gettext('Two password not equal')
        }]
    },
    old_password: {
        identifier  : 'old_password',
        rules: [{
            type   : 'empty',
            prompt : gettext('Please enter your current password')
        }]
    },
}