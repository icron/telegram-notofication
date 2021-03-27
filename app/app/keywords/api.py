import uuid

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user

from app.channels.model import Channels
from app.keywords.form import KeywordForm
from app.keywords.model import Keywords, Keyword


def keywords_blueprint(db):
    keywords = Blueprint('keywords', __name__)

    @keywords.route('/', methods=['GET'])
    def index() -> str:
        kw_list = Keywords(db).list()
        channels = Channels(db).all()
        ch_as_dict = Channels.list_to_dict(channels)
        for i, kw in enumerate(kw_list):
            ch_list = kw.channels.split(",")
            res = []
            for ch in ch_list:
                if ch in ch_as_dict:
                    res.append(ch_as_dict[ch].title)
                else:
                    res.append(ch)

            kw_list[i].channels = ",".join(res)

        return render_template('keywords/index.html', keywords=kw_list)

    @keywords.route('/create', methods=['GET', 'POST'])
    def create() -> str:
        form = KeywordForm()
        if form.validate_on_submit():
            k = Keyword(uuid=str(uuid.uuid4()), user_id=current_user.get_id(), channels=form.channels.data, keywords=form.keywords.data)
            Keywords(db).create(k)
            flash('Keyword successfully added')

            return redirect(url_for('keywords.index'))

        channels = Channels(db).all()

        return render_template('keywords/form.html', form=form, channels=channels)

    @keywords.route('/update/<uuid>', methods=['GET', 'POST'])
    def update(uuid: str) -> str:
        k_model = Keywords(db).get(uuid)
        form = KeywordForm(request.form, obj=k_model)

        if form.validate_on_submit():
            form.populate_obj(k_model)
            Keywords(db).update(k_model)
            flash('Keyword successfully updated')

            return redirect(url_for('keywords.index'))

        channels = Channels(db).all()

        return render_template('keywords/form.html', form=form, channels=channels)

    @keywords.route('/delete/<uuid>', methods=['POST'])
    def delete(uuid: str) -> str:
        Keywords(db).delete(uuid)
        flash('Keyword successfully deleted')

        return redirect(url_for('keywords.index'))

    return keywords
