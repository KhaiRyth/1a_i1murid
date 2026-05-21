# Menguatkuasakan keselamatan dengan mewujudkan pengguna bukan-root (Non-Root User Isolation)
RUN groupadd -r khairyth && useradd -r -g khairyth -s /bin/false security_agent
RUN mkdir -p /app/master_box/logs /app/master_box/secure_store && chown -r security_agent:khairyth /app

COPY --from=builder /root/.local /home/security_agent/.local
COPY --chown=security_agent:khairyth . .

ENV PATH=/home/security_agent/.local/bin:$PATH
ENV KR_RUNTIME_ENV=production
ENV ISO_42001_ENFORCEMENT=STRICT
ENV SECURITY_LOG_PATH=/app/master_box/logs/audit.log

USER security_agent

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import requests; res=requests.get('http://localhost:8080/health'); exit(0 if res.status_code==200 else 1)"

CMD ["python", "src/runtime_entry.py"]
