%rebase layout title='Register'
<div>
%if defined('message') and message:
    <div class="message"><p>{{message}}</p></div>
%else:
    <form method="post">
        <label for="id-nick">Nickname: </label>
        <input type="text" name="nick" maxlength="50" id="id-nick" tabindex="1"
        value="{{state['nick'] if defined('state') else ''}}"/>
        <br />
        <label for="id-email">E-mail: </label>
        <input type="text" name="email" id="id-email" tabindex="2"
        value="{{state['email'] if defined('state') else ''}}"/>
        <br />
        <label for="id-pass">Password: </label>
        <input type="password" name="password" id="id-pass" tabindex="3" />
        <br />
        <input type="submit" name="register" value="Register!" tabindex="4"/>
    </form>

    %if defined('error') and error:
        <div class="error">
            <p>{{error['msg']}} (#{{error['code']}})</p>
        </div>
    %end
%end
<br/><a href="/login">Log in</a>
</div>
