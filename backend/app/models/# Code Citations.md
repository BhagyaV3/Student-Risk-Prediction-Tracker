# Code Citations

## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(
```


## License: unknown
https://github.com/rati90/LMSwithFastAPI/blob/aaef3ba67295e937868f5a5fecbda9827073ab9e/db/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(
```


## License: unknown
https://github.com/levovit/StarNaviTestTask/blob/05a4ad3b6ce43b7bf18c92e1e1efcabc49eeb64f/app/models/user.py

```
Perfect! Now we need to **update the User model** to add the relationship to students.

**Update `backend/app/models/user.py`**

Find this line at the end of the imports section:
```python
from app.database.db import Base
```

And add after it:
```python
from sqlalchemy.orm import relationship
```

Then find this line inside the User class:
```python
    is_active = Column(Boolean, default=True)
```

Add this line right after it:
```python
    students = relationship("Student", back_populates="teacher")
```

Your updated User model should look like this (showing key changes):

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(
```

