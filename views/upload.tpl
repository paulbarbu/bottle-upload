%rebase layout title='Upload'
<div>
%if defined('nick') and nick:
    <p>Hello {{nick}}!</p>
%end

<p><a href="/logout">Log out</a></p>
</div>
