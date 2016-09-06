#!/usr/bin/env python
from app import app
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.run(debug=True, host='0.0.0.0')
