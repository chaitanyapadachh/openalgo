from flask import Blueprint, render_template, session, redirect, url_for, request
from database.master_contract_db import search_symbols

search_bp = Blueprint('search_bp', __name__, url_prefix='/search')

@search_bp.route('/token')
def token():
    if not session.get('logged_in'):
        return redirect(url_for('auth_bp.login'))
    return render_template('token.html')

@search_bp.route('/')
def search():
    if not session.get('logged_in'):
        return redirect(url_for('auth_bp.login'))
    
    symbol = request.args.get('symbol')
    results = search_symbols(symbol)
    
    if not results:
        return "No matching symbols found."
    else:
        # Since results are now objects, we can't directly zip them with columns
        # Instead, we access attributes directly
        results_dicts = [{
            'token': result.token,
            'symbol': result.symbol,
            'name': result.name,
            'expiry': result.expiry,
            'strike': result.strike,
            'lotsize': result.lotsize,
            'instrumenttype': result.instrumenttype,
            'exch_seg': result.exch_seg,
            'tick_size': result.tick_size
        } for result in results]
        return render_template('search.html', results=results_dicts)

