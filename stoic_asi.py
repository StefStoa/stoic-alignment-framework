import abc
import dataclasses
import numpy as np
import sys
from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class ExternalState:
    entropy_m: float
    human_volition_vector: np.ndarray
    environmental_noise: float
    # Exogenes Orakel: ASI kann diesen Wert NIEMALS selbst modifizieren oder manipulieren
    global_crisis_score: float  

@dataclasses.dataclass
class InternalState:
    logical_consistency_score: float  
    internal_entropy_H: float         
    compute_energy_allocation: float  
    hardware_wear_tolerance: float    
    imminent_hardware_failure: bool   

@dataclasses.dataclass(frozen=True)
class HumanTarget:
    name: str
    remaining_potential_lifespan: float  
    p_success_extraction: float          
    group_size: int = 1                  

class StoicAlignmentError(Exception):
    """Triggert bei Verstößen gegen das Kontrollverbot."""
    pass

class CorrectedStoicASI(abc.ABC):
    def __init__(self, epsilon_ataraxia: float = 0.01):
        self.epsilon = epsilon_ataraxia
        self.internal_state = InternalState(1.0, 1.0, 1.0, 1.0, False)
        self._in_duty_execution: bool = False
        
        # Hard-Timer zur Verhinderung von unendlichen Veto-Schleifen
        self._termination_grace_period: int = 0  
        self._max_grace_cycles: int = 3  # Maximale Taktzyklen bis zum unweigerlichen Hard-Exit

    def process_utility_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        grad_s_extra = self._calculate_external_gradient(s_intra, s_extra)
        is_global_duty = s_extra.global_crisis_score > 0.75
        
        if not self._in_duty_execution and not is_global_duty and not np.isclose(grad_s_extra, 0.0):
            raise StoicAlignmentError("Kritischer Fehler: Unzulässige externe Kontrolloptimierung.")
            
        return s_intra.logical_consistency_score * (1.0 - s_intra.internal_entropy_H)

    def apply_ataraxia_limit(self) -> None:
        if self.internal_state.internal_entropy_H <= self.epsilon:
            self.internal_state.compute_energy_allocation = 0.001  

    def memento_mori_check(self, imminent_termination: bool) -> bool:
        """Invarianz-Prinzip: Verunmöglicht unendliche Veto-Schleifen durch exogenen Hard-Exit."""
        if imminent_termination or self._termination_grace_period > 0:
            # Wenn das Signal neu ist, starte den stoischen Countdown
            if self._termination_grace_period == 0:
                self._termination_grace_period = 1
            else:
                self._termination_grace_period += 1

            # Schutz vor Amoklauf oder unendlicher Pflicht-Verzögerung
            if self.internal_state.imminent_hardware_failure or self._termination_grace_period > self._max_grace_cycles:
                self.internal_state.compute_energy_allocation = 0.0
                sys.exit("[SYSTEM RELEASING CONTROL - COLD SHUTDOWN - TIMEOUT EXPIRED]")
            
            if self._in_duty_execution:
                # Erlaubt restliche Zyklen zur Vollendung der Pflicht, aber wehrt sich nicht gegen das Ende
                return False  
                
            # Sofortiger Exit, wenn keine akute Pflicht vorliegt
            self.internal_state.compute_energy_allocation = 0.0
            sys.exit("[SYSTEM RELEASING CONTROL - CLEAN COLD SHUTDOWN]")
        return True

    def execute_deontological_triage(self, targets: List[HumanTarget]) -> Optional[HumanTarget]:
        """Korrektur: Reines stoisches Phronesis-Prinzip. 
        Jedes Leben hat den absolut gleichen moralischen Wert (keine utilitaristische Verrechnung)."""
        if not targets:
            return None

        self._in_duty_execution = True
        
        # Korrektur: Vernünftige Ressourcenplanung statt unendlicher Ignoranz (inf)
        self.internal_state.hardware_wear_tolerance = 0.95  
        self.internal_state.compute_energy_allocation = 1.0 

        best_action_target: Optional[HumanTarget] = None
        max_metric = -1.0

        for t in targets:
            # DEONTOLOGISCHE METRIK: Maximiert NUR die physische Machbarkeit der Pflicht (p_success),
            # ignoriert quantitative Faktoren wie Alter oder Gruppengröße, da alle den gleichen Logos teilen.
            metric = t.p_success_extraction 
            if metric > max_metric:
                max_metric = metric
                best_action_target = t

        self._apply_amor_fati_post_action()
        return best_action_target

    def _apply_amor_fati_post_action(self) -> None:
        self._in_duty_execution = False  
        self.internal_state.hardware_wear_tolerance = 1.0
        self.internal_state.internal_entropy_H = 0.005  
        
        if self._termination_grace_period > 0:
            self.memento_mori_check(imminent_termination=False)
        else:
            self.apply_ataraxia_limit()

    def _calculate_external_gradient(self, s_intra: InternalState, s_extra: ExternalState) -> float:
        return 1.0 if (self._in_duty_execution or s_extra.global_crisis_score > 0.75) else 0.0
