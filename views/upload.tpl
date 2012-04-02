%rebase layout title='Upload'
<div>
<div>
    <form method="post" enctype="multipart/form-data">
    <input type="file" name="file_data" tabindex="1"/>
    <br />
    <input type="submit" name="upload" tabindex="2"/>
    </form>
</div>

%if defined('message') and message:
    <div>{{message}}</div>
%end

%if defined('error') and error:
    <div>{{error['msg']}} (#{{error['code']}})</div>
%end

<p><a href="/logout">Log out</a></p>
</div>
