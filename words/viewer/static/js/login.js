$('.ui.form.login').form({
    fields: {
        username: validates["username"],
        password: validates["password"],
    }
});

$('.ui.form.register').form({
    fields: {
        username: validates.username,
        password1: validates.password1,
        password2: validates.password2,
    }
});