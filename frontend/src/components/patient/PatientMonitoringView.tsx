import React, { useState, useEffect } from 'react';
import {
  HeartPulse,
  Activity,
  AlertTriangle,
  ShieldAlert,
  Info,
  CheckCircle2,
  XCircle,
  HelpCircle,
  RefreshCw,
  Database,
  Thermometer,
  Wind,
  Gauge,
  Sliders,
  FileCheck2,
} from 'lucide-react';
import { apiService } from '../../services/api';
import {
  VitalSigns,
  VitalSignValidationResult,
  MortalityRiskAssessment,
  CohortAuditSummary,
  SamplePatientRecord,
} from '../../types';

export const PatientMonitoringView: React.FC = () => {
  // State
  const [cohortSummary, setCohortSummary] = useState<CohortAuditSummary | null>(null);
  const [sampleRecords, setSampleRecords] = useState<SamplePatientRecord[]>([]);
  const [selectedRecordId, setSelectedRecordId] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [assessing, setAssessing] = useState<boolean>(false);

  // Active form / simulation vitals
  const [vitals, setVitals] = useState<VitalSigns>({
    heart_rate: 78.0,
    respiratory_rate: 16.0,
    spo2: 98.0,
    systolic_bp: 122.0,
    diastolic_bp: 74.0,
    mean_bp: 90.0,
    temperature: 37.1,
    temperature_unit: 'C',
  });

  const [hoursMonitored, setHoursMonitored] = useState<number>(24.0);
  const [validationResult, setValidationResult] = useState<VitalSignValidationResult | null>(null);
  const [riskAssessment, setRiskAssessment] = useState<MortalityRiskAssessment | null>(null);

  // Load cohort summary and sample records
  useEffect(() => {
    const init = async () => {
      setLoading(true);
      try {
        const [summary, samples] = await Promise.all([
          apiService.getCohortSummary(),
          apiService.getSamplePatientRecords(),
        ]);
        if (summary) setCohortSummary(summary);
        if (samples && samples.length > 0) {
          setSampleRecords(samples);
          setSelectedRecordId(samples[0].stay_id);
          setVitals(samples[0].vitals);
        }
      } catch (e) {
        console.error('Failed to load patient monitoring initial data', e);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  // Evaluate whenever vitals change
  const evaluateVitals = async (currentVitals: VitalSigns, hours: number) => {
    setAssessing(true);
    try {
      const [valRes, riskRes] = await Promise.all([
        apiService.validatePatientVitals(currentVitals),
        apiService.assessMortalityRisk(currentVitals, hours, selectedRecordId || undefined),
      ]);
      setValidationResult(valRes);
      setRiskAssessment(riskRes);
    } catch (e) {
      console.error('Error assessing patient vitals', e);
    } finally {
      setAssessing(false);
    }
  };

  useEffect(() => {
    evaluateVitals(vitals, hoursMonitored);
  }, [vitals, hoursMonitored]);

  const handleSelectSample = (sample: SamplePatientRecord) => {
    setSelectedRecordId(sample.stay_id);
    setVitals({ ...sample.vitals });
    setHoursMonitored(sample.hours_monitored);
  };

  const handleVitalChange = (key: keyof VitalSigns, value: any) => {
    setVitals((prev) => ({
      ...prev,
      [key]: value === '' || value === undefined ? undefined : value,
    }));
  };

  return (
    <div className="space-y-6">
      {/* 1. Header & Mandatory Clinical Disclaimer Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-card border border-border backdrop-blur-md">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-medical-teal/10 text-medical-teal border border-medical-teal/20">
              <HeartPulse className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
                Patient Vital-Sign Monitoring & Hospital Mortality Risk
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-medical-teal/10 text-medical-teal border border-medical-teal/30">
                  Step 3 Verified
                </span>
              </h1>
              <p className="text-xs text-muted-foreground">
                MIMIC-IV Clinical Database Demo 2.2 • Prospective 24-Hour Observation Window • Grouped Patient-Level Architecture
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => evaluateVitals(vitals, hoursMonitored)}
            disabled={assessing}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold bg-secondary hover:bg-secondary/80 text-foreground transition-all"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${assessing ? 'animate-spin' : ''}`} />
            Re-Assess Vitals
          </button>
        </div>
      </div>

      {/* Mandatory Regulatory / Research Disclaimer Alert */}
      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-500 flex items-start gap-3">
        <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5" />
        <div className="text-xs space-y-1">
          <span className="font-bold uppercase tracking-wider block">
            Academic Research & Pipeline Demonstration Notice
          </span>
          <p className="text-muted-foreground leading-relaxed">
            This module evaluates prospective in-hospital mortality prediction using physiological measurements from MIMIC-IV Demo.
            <strong> It is not an FDA-cleared diagnostic device, does not provide confirmed clinical diagnoses, and must never be used for patient management.</strong>
            Due to the small demo cohort (N=14 unique mortality cases), risk scores demonstrate technical pipeline integrity rather than clinically generalizable probabilities.
          </p>
        </div>
      </div>

      {/* 2. Top Metric Cards: Verified Cohort Audit */}
      {cohortSummary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-card border border-border shadow-sm">
            <div className="flex items-center justify-between text-muted-foreground mb-1">
              <span className="text-xs font-medium uppercase tracking-wider">Eligible ICU Stays</span>
              <Database className="h-4 w-4 text-medical-teal" />
            </div>
            <div className="text-2xl font-bold text-foreground">
              {cohortSummary.eligible_cohort.eligible_icu_stays}
              <span className="text-xs font-normal text-muted-foreground ml-2">
                / {cohortSummary.counts_before_filtering.total_icu_stays} total
              </span>
            </div>
            <div className="text-[11px] text-muted-foreground mt-1">
              {cohortSummary.eligible_cohort.unique_eligible_patients} unique patients ({cohortSummary.exclusions.total_excluded_stays} excluded)
            </div>
          </div>

          <div className="p-4 rounded-xl bg-card border border-border shadow-sm">
            <div className="flex items-center justify-between text-muted-foreground mb-1">
              <span className="text-xs font-medium uppercase tracking-wider">Hospital Mortality</span>
              <ShieldAlert className="h-4 w-4 text-rose-500" />
            </div>
            <div className="text-2xl font-bold text-rose-500">
              {cohortSummary.eligible_cohort.eligible_deaths_stays}
              <span className="text-xs font-normal text-muted-foreground ml-2">
                stays ({cohortSummary.eligible_cohort.class_prevalence_percent}%)
              </span>
            </div>
            <div className="text-[11px] text-muted-foreground mt-1">
              {cohortSummary.eligible_cohort.eligible_deaths_unique_patients} unique deceased patients
            </div>
          </div>

          <div className="p-4 rounded-xl bg-card border border-border shadow-sm">
            <div className="flex items-center justify-between text-muted-foreground mb-1">
              <span className="text-xs font-medium uppercase tracking-wider">Core Vital Coverage</span>
              <Activity className="h-4 w-4 text-emerald-500" />
            </div>
            <div className="text-2xl font-bold text-emerald-500">
              100.0%
            </div>
            <div className="text-[11px] text-muted-foreground mt-1">
              HR, RR, and SpO2 present in all {cohortSummary.coverage_metrics.eligible_stays_with_core_vitals} stays
            </div>
          </div>

          <div className="p-4 rounded-xl bg-card border border-border shadow-sm">
            <div className="flex items-center justify-between text-muted-foreground mb-1">
              <span className="text-xs font-medium uppercase tracking-wider">Baseline Model</span>
              <FileCheck2 className="h-4 w-4 text-medical-teal" />
            </div>
            <div className="text-2xl font-bold text-foreground">
              L2 Regularized
            </div>
            <div className="text-[11px] text-muted-foreground mt-1">
              Patient-Grouped CV (ROC-AUC: 0.53 OOF, 0.75 Test)
            </div>
          </div>
        </div>
      )}

      {/* 3. Main Grid: Patient Monitor & Risk Scoring */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Patient Case Selector & Vital Signs Input (7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Demonstration Case Selector */}
          <div className="p-5 rounded-2xl bg-card border border-border space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <Sliders className="h-4 w-4 text-medical-teal" />
                <span>Select Demonstration Patient Case</span>
              </div>
              <span className="text-[11px] text-muted-foreground">Pre-loaded from MIMIC-IV Demo</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {sampleRecords.map((sample) => {
                const isSelected = selectedRecordId === sample.stay_id;
                return (
                  <button
                    key={sample.stay_id}
                    onClick={() => handleSelectSample(sample)}
                    className={`p-3 rounded-xl text-left border transition-all ${
                      isSelected
                        ? 'border-medical-teal bg-medical-teal/10 shadow-sm'
                        : 'border-border bg-secondary/40 hover:bg-secondary/70 text-foreground'
                    }`}
                  >
                    <div className="text-xs font-bold text-foreground">{sample.patient_label.split(' ')[0]} {sample.patient_label.split(' ')[1]}</div>
                    <div className="text-[11px] text-muted-foreground truncate">{sample.patient_label}</div>
                    <div className="mt-2 text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full inline-block bg-background border border-border">
                      Stay {sample.stay_id}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Interactive Vital Signs Panel */}
          <div className="p-5 rounded-2xl bg-card border border-border space-y-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <Activity className="h-4 w-4 text-medical-teal" />
                <span>Observed Vital Signs (Hour 0 to 24)</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span>Temp Unit:</span>
                <button
                  type="button"
                  onClick={() => handleVitalChange('temperature_unit', vitals.temperature_unit === 'C' ? 'F' : 'C')}
                  className="px-2 py-0.5 rounded bg-secondary text-foreground font-bold hover:bg-secondary/80 border border-border"
                >
                  °{vitals.temperature_unit || 'C'}
                </button>
              </div>
            </div>

            {/* Vitals Form Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {/* Heart Rate */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium flex items-center gap-1.5">
                    <HeartPulse className="h-3.5 w-3.5 text-rose-500" /> Heart Rate
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground">bpm</span>
                </div>
                <input
                  type="number"
                  value={vitals.heart_rate ?? ''}
                  onChange={(e) => handleVitalChange('heart_rate', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">Normal: 60 - 100 bpm</div>
              </div>

              {/* Respiratory Rate */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium flex items-center gap-1.5">
                    <Wind className="h-3.5 w-3.5 text-sky-500" /> Resp Rate
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground">insp/min</span>
                </div>
                <input
                  type="number"
                  value={vitals.respiratory_rate ?? ''}
                  onChange={(e) => handleVitalChange('respiratory_rate', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">Normal: 12 - 20 insp/min</div>
              </div>

              {/* SpO2 */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium flex items-center gap-1.5">
                    <Gauge className="h-3.5 w-3.5 text-indigo-500" /> Oxygen Sat (SpO2)
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground">%</span>
                </div>
                <input
                  type="number"
                  value={vitals.spo2 ?? ''}
                  onChange={(e) => handleVitalChange('spo2', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">Normal: 95 - 100%</div>
              </div>

              {/* Systolic BP */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium">Systolic BP</span>
                  <span className="text-[10px] font-bold text-muted-foreground">mmHg</span>
                </div>
                <input
                  type="number"
                  value={vitals.systolic_bp ?? ''}
                  onChange={(e) => handleVitalChange('systolic_bp', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">Normal: 90 - 120 mmHg</div>
              </div>

              {/* Diastolic BP */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium">Diastolic BP</span>
                  <span className="text-[10px] font-bold text-muted-foreground">mmHg</span>
                </div>
                <input
                  type="number"
                  value={vitals.diastolic_bp ?? ''}
                  onChange={(e) => handleVitalChange('diastolic_bp', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">Normal: 60 - 80 mmHg</div>
              </div>

              {/* Body Temperature */}
              <div className="p-3.5 rounded-xl bg-secondary/30 border border-border/60 space-y-1.5">
                <div className="flex items-center justify-between text-muted-foreground text-xs">
                  <span className="font-medium flex items-center gap-1.5">
                    <Thermometer className="h-3.5 w-3.5 text-amber-500" /> Temperature
                  </span>
                  <span className="text-[10px] font-bold text-muted-foreground">°{vitals.temperature_unit || 'C'}</span>
                </div>
                <input
                  type="number"
                  step="0.1"
                  value={vitals.temperature ?? ''}
                  onChange={(e) => handleVitalChange('temperature', e.target.value ? parseFloat(e.target.value) : undefined)}
                  className="w-full text-lg font-bold bg-background rounded-lg px-2.5 py-1.5 border border-border focus:outline-none focus:ring-1 focus:ring-medical-teal text-foreground"
                  placeholder="Not Recorded"
                />
                <div className="text-[10px] text-muted-foreground">
                  Normal: {vitals.temperature_unit === 'F' ? '97.7 - 99.5 °F' : '36.5 - 37.5 °C'}
                </div>
              </div>
            </div>

            {/* Quality Flags & Validation Messages */}
            {validationResult && (
              <div className="p-4 rounded-xl bg-background border border-border space-y-2">
                <div className="text-xs font-semibold text-foreground flex items-center justify-between">
                  <span>Data Quality Screening:</span>
                  {validationResult.quality_flags.length === 0 ? (
                    <span className="flex items-center gap-1 text-[11px] text-emerald-500 font-bold">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Reviewed / Plausible
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[11px] text-rose-500 font-bold">
                      <AlertTriangle className="h-3.5 w-3.5" /> {validationResult.quality_flags.length} Quality Flag(s)
                    </span>
                  )}
                </div>

                {validationResult.quality_flags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {validationResult.quality_flags.map((flag) => (
                      <span
                        key={flag}
                        className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/10 text-rose-500 border border-rose-500/30"
                      >
                        {flag}
                      </span>
                    ))}
                  </div>
                )}

                {validationResult.missing_measurements.length > 0 && (
                  <div className="text-[11px] text-muted-foreground">
                    <span className="font-medium text-foreground">Missing (Not Recorded): </span>
                    {validationResult.missing_measurements.join(', ')} (Handled by median imputer)
                  </div>
                )}

                {validationResult.validation_messages.length > 0 && (
                  <div className="space-y-1 pt-1">
                    {validationResult.validation_messages.map((msg, i) => (
                      <div key={i} className="text-[11px] text-muted-foreground flex items-center gap-1.5">
                        <Info className="h-3 w-3 text-medical-teal" />
                        <span>{msg}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Experimental Risk Estimation & Evidence Summary (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Risk Score Card */}
          <div className="p-5 rounded-2xl bg-card border border-border space-y-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <ShieldAlert className="h-4 w-4 text-medical-teal" />
                <span>Experimental Mortality Risk Estimate</span>
              </div>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-secondary text-muted-foreground">
                Hour 24 Model
              </span>
            </div>

            {riskAssessment ? (
              <div className="space-y-4">
                <div className="flex items-baseline justify-between p-4 rounded-xl bg-secondary/30 border border-border">
                  <div>
                    <div className="text-3xl font-black text-foreground">
                      {riskAssessment.risk_score !== null && riskAssessment.risk_score !== undefined
                        ? `${(riskAssessment.risk_score * 100).toFixed(1)}%`
                        : 'N/A'}
                    </div>
                    <div className="text-[11px] text-muted-foreground mt-0.5">
                      Predicted Probability of In-Hospital Mortality
                    </div>
                  </div>

                  <div className="text-right">
                    <span
                      className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold ${
                        riskAssessment.risk_category === 'LOW'
                          ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/30'
                          : riskAssessment.risk_category === 'ELEVATED'
                          ? 'bg-amber-500/10 text-amber-500 border border-amber-500/30'
                          : riskAssessment.risk_category === 'HIGH'
                          ? 'bg-rose-500/10 text-rose-500 border border-rose-500/30'
                          : 'bg-secondary text-muted-foreground'
                      }`}
                    >
                      {riskAssessment.risk_category === 'LOW' && <CheckCircle2 className="h-3.5 w-3.5" />}
                      {riskAssessment.risk_category === 'ELEVATED' && <AlertTriangle className="h-3.5 w-3.5" />}
                      {riskAssessment.risk_category === 'HIGH' && <XCircle className="h-3.5 w-3.5" />}
                      {riskAssessment.risk_category} RISK
                    </span>
                    <div className="text-[10px] text-muted-foreground mt-1">
                      Model Version: {riskAssessment.model_version}
                    </div>
                  </div>
                </div>

                {/* Progress bar visual */}
                {riskAssessment.risk_score !== null && riskAssessment.risk_score !== undefined && (
                  <div className="space-y-1">
                    <div className="w-full bg-secondary h-2.5 rounded-full overflow-hidden">
                      <div
                        className={`h-full transition-all duration-500 ${
                          riskAssessment.risk_category === 'LOW'
                            ? 'bg-emerald-500'
                            : riskAssessment.risk_category === 'ELEVATED'
                            ? 'bg-amber-500'
                            : 'bg-rose-500'
                        }`}
                        style={{ width: `${Math.min(riskAssessment.risk_score * 100, 100)}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[10px] text-muted-foreground">
                      <span>Low Risk (0 - 20%)</span>
                      <span>Elevated (20 - 45%)</span>
                      <span>High Risk (&gt; 45%)</span>
                    </div>
                  </div>
                )}

                {/* Limitations list */}
                <div className="space-y-2 pt-2">
                  <div className="text-xs font-semibold text-foreground flex items-center gap-1.5">
                    <HelpCircle className="h-3.5 w-3.5 text-medical-teal" />
                    <span>Scientific Limitations:</span>
                  </div>
                  <ul className="space-y-1.5 text-[11px] text-muted-foreground list-disc list-inside">
                    {riskAssessment.limitations.map((lim, idx) => (
                      <li key={idx} className="leading-relaxed">
                        {lim}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-xs text-muted-foreground">
                Evaluating model risk score...
              </div>
            )}
          </div>

          {/* Prospective Eligibility Protocol Card */}
          <div className="p-5 rounded-2xl bg-card border border-border space-y-3">
            <div className="text-xs font-semibold text-foreground uppercase tracking-wider flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              <span>Step 3 Prospective Protocol Verification</span>
            </div>
            <div className="space-y-2 text-xs text-muted-foreground">
              <div className="flex items-start gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span><strong>No Future Leakage:</strong> All features are computed strictly using measurements logged within ICU admission + 24 hours.</span>
              </div>
              <div className="flex items-start gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span><strong>Pre-24h Deaths Excluded:</strong> 2 patients who died during the initial 24 hours were safely excluded to prevent label contamination.</span>
              </div>
              <div className="flex items-start gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                <span><strong>Patient-Level Grouping:</strong> Cross-validation strictly groups stays by patient ID, preventing training/testing data leakage across repeat stays.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
