%rebase layout title='Login'
<div>
%if defined('message') and message:
    <div class="message">{{message}}</div>
%else:
    <form method="post">
        <label for="id-nick">Nickname: </label>
        <input type="text" name="nick" maxlength="50" id="id-nick" tabindex="1" />
        <br />
        <label for="id-pass">Password: </label>
        <input type="password" name="password" id="id-pass" tabindex="2" />
        <br />
        <input type="submit" name="login" value="Log in!" tabindex="3"/>
    </form>

    %if defined('error') and error:
        <div class="error">{{error['msg']}} (#{{error['code']}})</div>
    %end

    <p>
    If you don't have an account, you can create one on the <a href="/register">registration page</a>!
    </p>
%end
</div>

