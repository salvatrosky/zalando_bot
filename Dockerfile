FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
COPY . .
CMD ["python", "bot.py"]